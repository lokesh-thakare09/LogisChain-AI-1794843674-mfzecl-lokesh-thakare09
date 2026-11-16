"""Transparent financial calculations; values are illustrative, not advice."""
def expected_loss(pd: float, lgd: float, ead: float) -> float:
    for name, value in {"pd": pd, "lgd": lgd}.items():
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    if ead < 0:
        raise ValueError("ead cannot be negative")
    return pd * lgd * ead

def cash_conversion_cycle(dio: float, dso: float, dpo: float) -> float:
    return float(dio + dso - dpo)

def supply_chain_adjusted_pd(base_pd, otif_rate, lead_time_std, congestion, supplier_hhi):
    """Simple transparent demonstration overlay; calibrate before real use."""
    import math
    logit = math.log(max(base_pd, 1e-5) / max(1 - base_pd, 1e-5))
    stress = 1.4*(.9-otif_rate) + .035*lead_time_std + .08*congestion + .5*supplier_hhi
    z = logit + stress
    return 1 / (1 + math.exp(-z))

def indicative_scf_rate(base_rate, pd, lgd, operational_premium=0.005):
    return base_rate + pd * lgd + operational_premium
