"""Train CPU-friendly baselines and save honest holdout metrics."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score, brier_score_loss, mean_absolute_percentage_error, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "synthetic"
OUT = ROOT / "outputs"
MODEL = ROOT / "models"

def run():
    OUT.mkdir(exist_ok=True); MODEL.mkdir(exist_ok=True)
    suppliers = pd.read_csv(DATA / "suppliers.csv")
    feature_cols = [c for c in suppliers.select_dtypes(include="number").columns if c != "default_12m"]
    X, y = suppliers[feature_cols], suppliers["default_12m"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
    clf = Pipeline([("imputer", SimpleImputer(strategy="median")),
                    ("model", HistGradientBoostingClassifier(max_iter=120, learning_rate=.07, random_state=42))])
    clf.fit(Xtr, ytr)
    proba = clf.predict_proba(Xte)[:, 1]
    metrics = {
        "supplier_default_auc": float(roc_auc_score(yte, proba)) if yte.nunique() > 1 else None,
        "supplier_default_brier": float(brier_score_loss(yte, proba)),
        "supplier_default_accuracy_at_0_5": float(accuracy_score(yte, proba >= .5)),
        "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
        "data_type": "synthetic demonstration data",
    }
    joblib.dump({"model": clf, "features": feature_cols}, MODEL / "supplier_default.joblib")

    ships = pd.read_csv(DATA / "shipments.csv")
    ship_features = ["distance_km", "cargo_value_usd", "route_congestion", "weather_severity",
                     "documentation_errors", "carrier_reliability"]
    Xs, ys = ships[ship_features], ships["delay"]
    Xtr, Xte, ytr, yte = train_test_split(Xs, ys, test_size=.25, random_state=42, stratify=ys)
    ship_model = Pipeline([("imputer", SimpleImputer(strategy="median")),
                           ("model", HistGradientBoostingClassifier(max_iter=100, random_state=42))])
    ship_model.fit(Xtr, ytr)
    ps = ship_model.predict_proba(Xte)[:, 1]
    metrics["shipment_delay_auc"] = float(roc_auc_score(yte, ps))
    metrics["shipment_delay_brier"] = float(brier_score_loss(yte, ps))
    joblib.dump({"model": ship_model, "features": ship_features}, MODEL / "shipment_delay.joblib")

    ts = pd.read_csv(DATA / "daily_timeseries.csv")
    # One-step lagged baseline; chronological split.
    yts = ts["port_throughput_teu"]
    frame = pd.DataFrame({"lag1": yts.shift(1), "lag7": yts.shift(7),
                          "lag30": yts.shift(30), "day": np.arange(len(yts))})
    frame["target"] = yts
    frame = frame.dropna()
    cut = int(len(frame) * .8)
    reg = Pipeline([("imputer", SimpleImputer(strategy="median")),
                    ("model", RandomForestRegressor(n_estimators=100, min_samples_leaf=3, random_state=42))])
    reg.fit(frame.iloc[:cut][["lag1","lag7","lag30","day"]], frame.iloc[:cut]["target"])
    pred = reg.predict(frame.iloc[cut:][["lag1","lag7","lag30","day"]])
    metrics["throughput_holdout_mape"] = float(mean_absolute_percentage_error(frame.iloc[cut:]["target"], pred))
    joblib.dump(reg, MODEL / "throughput_baseline.joblib")
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    return metrics

if __name__ == "__main__":
    if not (DATA / "suppliers.csv").exists():
        from src.data.generate import generate
        generate()
    run()
