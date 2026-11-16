"""Combine operational indicators with financial risk outputs."""
from .risk import expected_loss, cash_conversion_cycle, supply_chain_adjusted_pd, indicative_scf_rate

def assess_exposure(financials, supply_chain, ead):
    base_pd = float(financials.get("base_pd", .03))
    pd_adj = supply_chain_adjusted_pd(
        base_pd, float(supply_chain["otif_rate"]), float(supply_chain["lead_time_std"]),
        float(supply_chain["port_congestion"]), float(supply_chain["supplier_hhi"])
    )
    lgd = float(financials.get("lgd", .45))
    ccc = cash_conversion_cycle(float(financials["dio"]), float(financials["dso"]), float(financials["dpo"]))
    return {
        "base_pd": base_pd, "supply_chain_adjusted_pd": pd_adj, "lgd": lgd,
        "ead": float(ead), "expected_loss": expected_loss(pd_adj, lgd, float(ead)),
        "cash_conversion_cycle_days": ccc,
        "indicative_scf_rate": indicative_scf_rate(float(financials.get("base_rate", .06)), pd_adj, lgd)
    }
