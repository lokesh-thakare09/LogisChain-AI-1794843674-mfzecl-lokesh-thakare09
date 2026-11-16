# LogisChain AI — Technical Report (working draft)

## 1. Problem statement
Trade-finance and working-capital decisions often rely heavily on borrower financial statements. Logistics disruption can change delivery reliability, inventory buffers, cash conversion cycles, documentary settlement timing, and ultimately borrower credit risk. LogisChain AI demonstrates how operational supply-chain signals can be incorporated into financial risk assessment.

## 2. Proposed architecture
**Physical data layer:** suppliers, manufacturers, ports, warehouses, shipments, freight rates, throughput and disruption events.  
**Intelligence layer:** graph topology features, shipment-delay classification, throughput forecasting and tabular borrower-risk estimation.  
**Financial layer:** PD/LGD/EAD, expected loss, CCC decomposition and indicative SCF pricing.  
**Simulation layer:** weekly portfolio decisions, scenario shocks and scorecard.

## 3. Data
The default repository uses generated synthetic data. It includes 240 suppliers, 3,000 shipments and 730 daily observations. This supports software testing only. For the final empirical study, replace it with licensed/public data and document provenance, retrieval dates, definitions, missingness and limitations.

## 4. Models
- **Graph:** heterogeneous node/edge types and NetworkX topology measures. The optional PyTorch architecture provides a three-layer attention-style message-passing template. For the final HetGAT experiment, use PyTorch Geometric `HeteroData`, at least three node types, four relation types and a time-aware edge split.
- **Temporal:** lagged random-forest baseline; optional dilated TCN template with three quantiles and multiple forecast horizons.
- **Shipment:** gradient-boosting baseline; optional Transformer encoder with four attention heads and attention pooling.
- **Financial risk:** transparent supply-chain-adjusted PD overlay and expected-loss calculation. This is a demonstration formula, not a calibrated lending model.

## 5. Evaluation protocol
The baseline script reports AUC and Brier score for classification and MAPE for throughput. It uses a stratified random holdout for the synthetic cross-sectional classification and a chronological holdout for the time series. A final real-data study must use borrower/entity- and time-aware splits to prevent leakage, calibration curves/ECE, confidence intervals, stability analysis, subgroup tests, and comparison against financial-only baselines.

## 6. Financial formulas
`EL = PD × LGD × EAD`  
`CCC = DIO + DSO − DPO`  
`SCF rate = base rate + PD × LGD + operational premium`

These calculations are simplified and exclude regulatory capital, funding costs, collateral, tenor, recovery timing, legal enforceability, concentration add-ons and institution-specific policy.

## 7. Simulation
LogisChain Lab implements two mandatory modes, ten disruption types, weekly turns and a five-part 1,000-point score. Each event produces freight, delay, inventory, LC-expiry and insurance-related impacts. Scenario parameters and loss coefficients are illustrative and should be calibrated with domain experts.

## 8. Limitations and responsible use
Synthetic outcomes are not evidence of predictive validity. The application must not be used to approve/decline credit, price a real facility, or make investment/insurance decisions. Validate with representative data, independent review, explainability, fairness, security, audit trails and applicable regulatory requirements.

## 9. Experiments to add before final submission
1. Compare financial-only vs financial + logistics features.
2. Train a true heterogeneous GAT on typed graph data.
3. Train the TCN on at least two documented time series and report 30/60/90-day quantile metrics.
4. Train the shipment Transformer on event sequences and report ROC-AUC, Brier and calibration.
5. Run temporal default backtests; report Gini, ECE, C-index and uncertainty.
6. Add SHAP global/local explanations where supported by the selected estimator.
7. Record all seeds, environment versions, model parameters and data versions.
