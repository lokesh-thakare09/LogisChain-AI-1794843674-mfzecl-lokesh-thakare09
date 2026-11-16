import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
import json
import pandas as pd
import streamlit as st
from src.data.generate import generate
from src.supply_chain.graph import build_network, graph_features, network_summary
from src.finance.integrate import assess_exposure
from src.simulation.engine import SimulationEngine
from src.simulation.scenarios import SCENARIOS

st.set_page_config(page_title="LogisChain AI", page_icon="🚢", layout="wide")
st.title("🚢 LogisChain AI")
st.caption("Predictive Trade Finance & Logistics Valuation | Synthetic-data demonstration")

data_dir = ROOT / "data" / "synthetic"
if not (data_dir / "suppliers.csv").exists():
    generate()
suppliers = pd.read_csv(data_dir / "suppliers.csv")
shipments = pd.read_csv(data_dir / "shipments.csv")
ts = pd.read_csv(data_dir / "daily_timeseries.csv", parse_dates=["date"])

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Network intelligence", "Financial risk", "LogisChain Lab"])
with tab1:
    st.warning("All displayed data is synthetic demonstration data. It is not a real credit decision or investment recommendation.")
    a,b,c,d = st.columns(4)
    a.metric("Suppliers", f"{len(suppliers):,}")
    b.metric("Shipments", f"{len(shipments):,}")
    c.metric("Synthetic default rate", f"{suppliers.default_12m.mean():.1%}")
    d.metric("Synthetic shipment delay rate", f"{shipments.delay.mean():.1%}")
    st.subheader("Port throughput and freight index")
    st.line_chart(ts.set_index("date")[["port_throughput_teu","freight_index"]])
    metrics_path = ROOT / "outputs" / "metrics.json"
    if metrics_path.exists():
        st.subheader("Measured holdout metrics")
        st.json(json.loads(metrics_path.read_text()))
    else:
        st.info("Run `python -m src.models.train_baselines` to train baselines and produce measured holdout metrics.")

with tab2:
    G = build_network()
    summary = network_summary(G)
    x,y,z = st.columns(3)
    x.metric("Network nodes", summary["nodes"])
    y.metric("Network links", summary["edges"])
    z.metric("Node types", len(summary["node_types"]))
    st.write("Node types:", ", ".join(summary["node_types"]))
    st.write("Relationship types:", ", ".join(summary["edge_types"]))
    st.dataframe(graph_features(G).sort_values("betweenness", ascending=False).head(20), use_container_width=True)

with tab3:
    st.subheader("Supply-chain-adjusted borrower risk")
    col1,col2 = st.columns(2)
    with col1:
        base_pd = st.slider("Financial-only PD", .001, .30, .03, .001)
        lgd = st.slider("Loss Given Default", .05, .90, .45, .01)
        ead = st.number_input("Exposure at Default (USD)", min_value=10000, value=2_000_000, step=10000)
        dio = st.slider("Days Inventory Outstanding", 1, 180, 55)
        dso = st.slider("Days Sales Outstanding", 1, 180, 42)
        dpo = st.slider("Days Payable Outstanding", 1, 180, 32)
    with col2:
        otif = st.slider("OTIF rate", .40, 1.0, .90)
        ltstd = st.slider("Lead-time standard deviation (days)", .1, 20., 4.5)
        congestion = st.slider("Port congestion (0–5)", 0., 5., 2.1)
        hhi = st.slider("Supplier concentration HHI", 0., 1., .25)
    result = assess_exposure({"base_pd":base_pd,"lgd":lgd,"dio":dio,"dso":dso,"dpo":dpo,"base_rate":.06},
                             {"otif_rate":otif,"lead_time_std":ltstd,"port_congestion":congestion,"supplier_hhi":hhi}, ead)
    st.metric("Supply-chain-adjusted PD", f"{result['supply_chain_adjusted_pd']:.2%}")
    st.metric("Expected loss", f"${result['expected_loss']:,.0f}")
    st.metric("Cash conversion cycle", f"{result['cash_conversion_cycle_days']:.1f} days")
    st.metric("Indicative SCF annual rate", f"{result['indicative_scf_rate']:.2%}")
    st.caption("Illustrative transparent overlay; calibrate, validate and obtain compliance approval before any real use.")

with tab4:
    if "engine" not in st.session_state:
        st.session_state.engine = SimulationEngine()
    engine = st.session_state.engine
    st.subheader("Weekly disruption-response simulation")
    mode = st.selectbox("Game mode", ["Trade Finance Portfolio Management","Supply Chain Finance Pricing"])
    if st.button("Start / reset game"):
        engine.new_game(mode)
    st.write(f"Week: {engine.state.week} / 52 | Portfolio: ${engine.state.portfolio_m:,.2f}M | CCC: {engine.state.ccc_days:.1f} days")
    scenario_names = [x["name"] for x in SCENARIOS]
    scenario_idx = st.selectbox("Disruption scenario", range(len(scenario_names)), format_func=lambda i: scenario_names[i])
    action = st.selectbox("Decision", ["monitor","extend_lc","diversify","working_capital","reprice"],
                          format_func=lambda x: {"monitor":"Monitor / use risk signals","extend_lc":"Extend letter of credit","diversify":"Diversify routes / carriers","working_capital":"Arrange working-capital facility","reprice":"Reprice financing"}[x])
    if st.button("Apply decision for this week"):
        result = engine.apply_week(scenario_idx, action)
        st.success(f"{result['scenario']['name']} applied. Estimated modelled loss: ${result['gross_loss_m']:.3f}M")
        st.json({k:round(v,3) for k,v in result.items() if k.endswith("_m")})
    st.subheader("Scorecard (maximum 1,000 points)")
    st.json(engine.score())
    if engine.state.history:
        st.dataframe(pd.DataFrame(engine.state.history), use_container_width=True)
    st.caption("Scenario loss equations and scoring are simplified educational mechanics, not bank-grade valuation.")
