"""Create deterministic synthetic supply-chain and finance demo datasets."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "synthetic"

def generate(seed: int = 42, n_suppliers: int = 240, n_shipments: int = 3000):
    rng = np.random.default_rng(seed)
    OUT.mkdir(parents=True, exist_ok=True)

    suppliers = pd.DataFrame({
        "supplier_id": [f"S{i:04d}" for i in range(n_suppliers)],
        "country": rng.choice(["IN", "CN", "US", "DE", "SG", "NL"], n_suppliers),
        "sector": rng.choice(["electronics", "automotive", "food", "textiles", "medical"], n_suppliers),
        "current_ratio": np.clip(rng.normal(1.65, .45, n_suppliers), .4, 3.5),
        "debt_to_equity": np.clip(rng.lognormal(-.1, .55, n_suppliers), .05, 5),
        "otif_rate": np.clip(rng.normal(.91, .08, n_suppliers), .45, 1),
        "lead_time_days": np.clip(rng.normal(24, 8, n_suppliers), 3, 70),
        "lead_time_std": np.clip(rng.normal(4.5, 2, n_suppliers), .5, 15),
        "port_congestion": np.clip(rng.normal(2.1, .9, n_suppliers), 0, 5),
        "freight_cost_ratio": np.clip(rng.normal(.12, .05, n_suppliers), .01, .4),
        "inventory_turnover": np.clip(rng.normal(6, 2, n_suppliers), .5, 15),
        "supplier_hhi": np.clip(rng.beta(2, 5, n_suppliers), 0, 1),
        "customer_hhi": np.clip(rng.beta(2, 5, n_suppliers), 0, 1),
        "revenue_growth": rng.normal(.07, .12, n_suppliers),
        "ebitda_margin": np.clip(rng.normal(.13, .07, n_suppliers), -.2, .4),
    })
    latent = (
        1.2 * (1.4 - suppliers.current_ratio)
        + .55 * suppliers.debt_to_equity
        + 2.2 * (0.9 - suppliers.otif_rate)
        + .08 * suppliers.lead_time_std
        + .25 * suppliers.port_congestion
        + .7 * suppliers.supplier_hhi
        - 1.1
    )
    p_default = 1 / (1 + np.exp(-latent))
    suppliers["default_12m"] = rng.binomial(1, np.clip(p_default, .01, .65))
    suppliers.to_csv(OUT / "suppliers.csv", index=False)

    sid = rng.integers(0, n_suppliers, n_shipments)
    delay_risk = (
        .9 * (1 - suppliers.otif_rate.to_numpy()[sid])
        + .035 * suppliers.lead_time_std.to_numpy()[sid]
        + .07 * suppliers.port_congestion.to_numpy()[sid]
        + rng.normal(0, .12, n_shipments)
    )
    p_delay = 1 / (1 + np.exp(-(-1.8 + 4 * delay_risk)))
    shipments = pd.DataFrame({
        "shipment_id": [f"SH{i:06d}" for i in range(n_shipments)],
        "supplier_id": suppliers.supplier_id.to_numpy()[sid],
        "distance_km": np.clip(rng.normal(6200, 2800, n_shipments), 100, 18000),
        "cargo_value_usd": np.clip(rng.lognormal(11.2, .8, n_shipments), 1000, 2_000_000),
        "route_congestion": np.clip(rng.normal(2.2, 1.0, n_shipments), 0, 5),
        "weather_severity": rng.integers(0, 6, n_shipments),
        "documentation_errors": rng.poisson(.18, n_shipments),
        "carrier_reliability": np.clip(rng.normal(.9, .08, n_shipments), .5, 1),
        "delay_days": np.clip(rng.gamma(2, 2, n_shipments), 0, 45).round(1),
        "delay": rng.binomial(1, np.clip(p_delay, .01, .9)),
    })
    shipments.to_csv(OUT / "shipments.csv", index=False)

    dates = pd.date_range("2021-01-01", periods=730, freq="D")
    seasonal = 1000 + 130 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365.25)
    trend = np.arange(len(dates)) * .12
    noise = rng.normal(0, 55, len(dates))
    disruption = np.zeros(len(dates))
    for start in [180, 420, 610]:
        disruption[start:start+12] -= rng.uniform(180, 300)
    throughput = np.maximum(100, seasonal + trend + noise + disruption)
    freight = np.maximum(300, 900 + 100*np.sin(np.arange(len(dates))*2*np.pi/180) + rng.normal(0, 45, len(dates)) - disruption*.8)
    ts = pd.DataFrame({"date": dates, "port_throughput_teu": throughput.round(2), "freight_index": freight.round(2)})
    ts.to_csv(OUT / "daily_timeseries.csv", index=False)
    print(f"Synthetic datasets written to {OUT}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    generate(seed=args.seed)
