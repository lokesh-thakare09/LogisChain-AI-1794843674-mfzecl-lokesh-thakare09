# Model Card — LogisChain AI demonstration

## Intended use
Educational prototype for exploring relationships between logistics operations and financial risk.

## Out-of-scope use
Real credit underwriting, trade-finance approval, insurance underwriting, regulatory capital calculation, or automated adverse decisions.

## Data
Synthetic generated data by default. No real people, borrowers, banks, carriers or shipments are represented.

## Models
- Supplier default classifier: HistGradientBoostingClassifier baseline.
- Shipment delay classifier: HistGradientBoostingClassifier baseline.
- Throughput forecast: lag-feature RandomForestRegressor.
- Optional architectures: PyTorch graph attention-style message passing, TCN, Transformer.

## Performance
Metrics are produced by running `python -m src.models.train_baselines`. No performance claims are made in advance. Synthetic metrics must not be presented as real-world model performance.

## Risks
Synthetic-to-real domain shift, target leakage, selection bias, class imbalance, calibration drift, proxy discrimination, missing operational data, and overreliance on a single supplier/port feature.

## Monitoring plan
Monitor feature distributions, missingness, prediction drift, calibration, false-negative rate, subgroup performance and realised default/delay outcomes. Establish thresholds and human review before deployment.
