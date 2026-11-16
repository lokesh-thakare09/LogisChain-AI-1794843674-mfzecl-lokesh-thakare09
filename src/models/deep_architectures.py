"""Optional PyTorch architecture templates; install requirements-advanced.txt first.

These modules are research templates, not trained/prevalidated production models.
"""
try:
    import torch
    from torch import nn
except ImportError as exc:
    raise ImportError("Install PyTorch with: pip install -r requirements-advanced.txt") from exc

class DilatedTCN(nn.Module):
    def __init__(self, input_dim=2, channels=32, horizons=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(input_dim, channels, 3, padding=2, dilation=1),
            nn.ReLU(),
            nn.Conv1d(channels, channels, 3, padding=4, dilation=2),
            nn.ReLU(),
            nn.Conv1d(channels, channels, 3, padding=8, dilation=4),
            nn.ReLU(),
        )
        self.head = nn.Linear(channels, horizons * 3)  # 10th, 50th, 90th quantiles
        self.horizons = horizons
    def forward(self, x):
        z = self.net(x)[:, :, -1]
        return self.head(z).view(-1, self.horizons, 3)

class ShipmentTransformer(nn.Module):
    def __init__(self, input_dim=8, d_model=32, heads=4, layers=2):
        super().__init__()
        self.proj = nn.Linear(input_dim, d_model)
        layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=heads, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=layers)
        self.attn_head = nn.Sequential(nn.Linear(d_model, 1))
        self.classifier = nn.Linear(d_model, 1)
    def forward(self, x):
        h = self.encoder(self.proj(x))
        weights = torch.softmax(self.attn_head(h), dim=1)
        pooled = (h * weights).sum(dim=1)
        return torch.sigmoid(self.classifier(pooled)), weights.squeeze(-1)

class HeterogeneousAttentionBaseline(nn.Module):
    """Type-aware attention-style message aggregation without PyG dependency.

    Inputs are node feature matrix and edge_index; use separate node-type embeddings
    and edge-type embeddings in a production PyG/HeteroData implementation.
    """
    def __init__(self, in_features=8, hidden=32, node_types=4, edge_types=4):
        super().__init__()
        self.node_type_embedding = nn.Embedding(node_types, 8)
        self.edge_type_embedding = nn.Embedding(edge_types, 8)
        self.input = nn.Linear(in_features + 8, hidden)
        self.layers = nn.ModuleList([nn.Linear(hidden * 2, hidden) for _ in range(3)])
        self.attn = nn.ModuleList([nn.Linear(hidden * 2, 1) for _ in range(3)])
        self.output = nn.Linear(hidden, 1)
    def forward(self, x, node_type, edge_index, edge_type):
        h = torch.relu(self.input(torch.cat([x, self.node_type_embedding(node_type)], dim=-1)))
        src, dst = edge_index
        for layer, attn in zip(self.layers, self.attn):
            pair = torch.cat([h[src] + self.edge_type_embedding(edge_type), h[dst]], dim=-1)
            score = torch.sigmoid(attn(pair))
            agg = torch.zeros_like(h)
            denom = torch.zeros((h.size(0), 1), device=h.device)
            agg.index_add_(0, dst, score * h[src])
            denom.index_add_(0, dst, score)
            agg = agg / denom.clamp_min(1e-6)
            h = torch.relu(layer(torch.cat([h, agg], dim=-1)))
        return torch.sigmoid(self.output(h))
