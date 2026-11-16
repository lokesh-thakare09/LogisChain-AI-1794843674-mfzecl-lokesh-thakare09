"""Synthetic multi-entity supply-chain graph and topology features."""
import numpy as np
import pandas as pd
import networkx as nx

def build_network(n_suppliers=220, n_manufacturers=35, n_ports=18, n_warehouses=30, seed=42):
    rng = np.random.default_rng(seed)
    G = nx.DiGraph()
    groups = {
        "supplier": [f"S{i:03d}" for i in range(n_suppliers)],
        "manufacturer": [f"M{i:03d}" for i in range(n_manufacturers)],
        "port": [f"P{i:03d}" for i in range(n_ports)],
        "warehouse": [f"W{i:03d}" for i in range(n_warehouses)],
    }
    for kind, nodes in groups.items():
        for node in nodes:
            G.add_node(node, node_type=kind, risk=float(rng.uniform(.02, .35)))
    # Supplier -> manufacturer
    for s in groups["supplier"]:
        for m in rng.choice(groups["manufacturer"], size=int(rng.integers(3, 6)), replace=False):
            G.add_edge(s, m, edge_type="supplies", weight=float(rng.uniform(.2, 1)))
    # Manufacturer -> port -> warehouse and some direct lanes
    for m in groups["manufacturer"]:
        p = rng.choice(groups["port"])
        G.add_edge(m, p, edge_type="exports_through", weight=float(rng.uniform(.2, 1)))
    for p in groups["port"]:
        for w in rng.choice(groups["warehouse"], size=int(rng.integers(8, 16)), replace=False):
            G.add_edge(p, w, edge_type="ships_to", weight=float(rng.uniform(.2, 1)))
    for w in groups["warehouse"]:
        for m in rng.choice(groups["manufacturer"], size=2, replace=False):
            G.add_edge(w, m, edge_type="replenishes", weight=float(rng.uniform(.2, 1)))
    return G

def graph_features(G):
    und = G.to_undirected()
    degree = dict(G.degree())
    betweenness = nx.betweenness_centrality(G, normalized=True)
    pagerank = nx.pagerank(G)
    rows = []
    for node, attrs in G.nodes(data=True):
        rows.append({
            "entity_id": node,
            "node_type": attrs["node_type"],
            "degree": degree[node],
            "betweenness": betweenness[node],
            "pagerank": pagerank[node],
            "risk_prior": attrs["risk"],
            "clustering": nx.clustering(und, node),
        })
    return pd.DataFrame(rows)

def network_summary(G):
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
            "node_types": sorted({d["node_type"] for _, d in G.nodes(data=True)}),
            "edge_types": sorted({d["edge_type"] for _, _, d in G.edges(data=True)})}
