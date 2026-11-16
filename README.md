# LogisChain AI — Predictive Trade Finance & Logistics Valuation

**Private academic project scaffold / runnable CPU-first MVP.**  
LogisChain AI combines supply-chain network intelligence, disruption forecasting, shipment risk, and financial risk calculations. LogisChain Lab is a turn-based simulation for trade-finance and supply-chain-finance decisions.

> **Confidentiality:** Keep this repository private. Do not publish the code, project brief, implementation, screenshots, or datasets. Use only data you are authorised to use. Never commit credentials or confidential employer/customer information.

## What is implemented

- Reproducible synthetic dataset generator (clearly labelled synthetic records).
- Supply-chain graph generation and topology features (200+ nodes / 1,000+ edges by default).
- CPU baseline models: shipment delay classifier, supplier default classifier, and multi-horizon throughput forecasting.
- Optional PyTorch architecture definitions: heterogeneous graph attention-style network, dilated TCN, and Transformer encoder with attention weights.
- Financial engine: PD, LGD, EAD, expected loss, CCC decomposition, and indicative SCF pricing.
- LogisChain Lab: 100+ nodes / 500+ links, 10 disruption scenarios, weekly turns, mandatory Trade Finance Portfolio Management and Supply Chain Finance Pricing modes, 1,000-point scoring.
- Streamlit dashboard and tests.

## Important model limitations

The included data generator creates **synthetic data** for software development and demonstration. It does not establish real-world predictive performance. Model metrics are computed when you run training; do not claim target AUC/MAPE/Gini/C-index values unless your measured test results support them. The optional deep-learning modules are architecture templates and need real training data and validation. The default pipeline is CPU-friendly and deliberately avoids requiring a GPU.

## Quick start

Python 3.10–3.12 recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m src.data.generate
python -m src.models.train_baselines
streamlit run app/dashboard.py
```

Open the local Streamlit URL shown in the terminal.

## Docker

```bash
docker compose up --build
```

## Repository map

```text
LogisChain-AI/
├── app/                  # Streamlit dashboard
├── configs/              # Project defaults
├── data/                 # Generated data (ignored by Git)
├── docs/                 # Technical note, model card, patent concept
├── outputs/              # Metrics and model artefacts (ignored by Git)
├── src/
│   ├── data/             # Synthetic data and validation
│   ├── supply_chain/     # Network graph and features
│   ├── models/           # Baselines and optional deep models
│   ├── finance/          # Financial formulas and risk integration
│   └── simulation/       # Scenario engine and game modes
└── tests/
```

## Data sources to connect after the MVP

Use official APIs / open datasets and respect each provider's terms:
- UN Comtrade: https://comtradeapi.un.org/
- World Bank Data: https://data.worldbank.org/
- SEC EDGAR: https://www.sec.gov/edgar/search/
- Port of Los Angeles open data: https://data.portoflosangeles.org/

Do not scrape restricted services or commit API keys. Add source, licence, retrieval date, units, and transformations to a data dictionary. Synthetic shipment rows must never be represented as observed AIS or customs data.

## Reproducibility

```bash
python -m src.data.generate --seed 42
python -m src.models.train_baselines
pytest -q
```

The training script writes metrics to `outputs/metrics.json`. Use a chronological split for time-dependent data. This demonstration uses a reproducible synthetic holdout and is not a production credit model.

## Financial definitions

- Expected Loss: `EL = PD × LGD × EAD`
- Cash Conversion Cycle: `CCC = DIO + DSO − DPO`
- Indicative annualised SCF rate: `base_rate + PD × LGD + operational_premium`

All values are illustrative. Actual pricing requires institution-specific policy, capital, liquidity, legal, and regulatory inputs.

## Security and submission checklist

- [ ] Keep GitHub repository private; grant access only to authorised collaborators.
- [ ] Add `.env` to `.gitignore`; commit only `.env.example`.
- [ ] Review Zetheta's ownership-transfer instructions and exact deadline before transferring.
- [ ] Run `pytest -q`; target at least 60% coverage as specified in the brief.
- [ ] Record measured metrics and data provenance; do not fabricate results.
- [ ] Build Docker image and verify `docker compose up`.
- [ ] Add architecture diagrams, screenshots, API docs, and a 15–20 page technical report based on actual experiments.
- [ ] Confirm any stale project-name references in the supplied submission checklist with the supervisor.
- [ ] Remove personal copies only if explicitly required by the official transfer process.

## Suggested next steps for a research-grade submission

1. Replace synthetic inputs with documented public datasets.
2. Add entity resolution and point-in-time feature generation.
3. Train and compare the baseline against the optional GNN / TCN / Transformer.
4. Perform time-based backtesting, calibration, confidence intervals, and subgroup/bias checks.
5. Add MLflow, DVC, CI, and model monitoring once the core pipeline is stable.
