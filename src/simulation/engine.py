"""Turn-based LogisChain Lab simulation engine."""
from dataclasses import dataclass, field
import random
from .scenarios import SCENARIOS
from src.supply_chain.graph import build_network, network_summary

@dataclass
class GameState:
    mode: str = "Trade Finance Portfolio Management"
    week: int = 1
    cash_m: float = 50.0
    portfolio_m: float = 500.0
    yield_rate: float = .015
    npl_ratio: float = .02
    ccc_days: float = 65.0
    risk_score: float = 50.0
    supply_chain_usage: float = 0.0
    decisions: int = 0
    financial_score: float = 150.0
    risk_score_points: float = 125.0
    intelligence_points: float = 100.0
    speed_points: float = 50.0
    learning_points: float = 75.0
    history: list = field(default_factory=list)

class SimulationEngine:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.graph = build_network(n_suppliers=100, n_manufacturers=20, n_ports=12, n_warehouses=20, seed=seed)
        self.state = GameState()

    def network_info(self):
        return network_summary(self.graph)

    def new_game(self, mode):
        if mode not in ["Trade Finance Portfolio Management", "Supply Chain Finance Pricing"]:
            raise ValueError("Unsupported game mode")
        self.state = GameState(mode=mode)
        return self.state

    def apply_week(self, scenario_index=None, action="monitor"):
        s = self.state
        scenario = SCENARIOS[scenario_index if scenario_index is not None else self.rng.randrange(len(SCENARIOS))]
        exposure = s.portfolio_m
        freight_cost = exposure * .025 * scenario["freight_pct"]
        delay_loss = exposure * .0008 * scenario["delay_days"]
        inventory_cost = exposure * .00025 * scenario["inventory_days"]
        lc_loss = exposure * scenario["lc_expiry"] * .004
        claim_loss = exposure * scenario["insurance_claim"] * .002
        gross_loss = max(0, freight_cost + delay_loss + inventory_cost + lc_loss + claim_loss)

        if action == "extend_lc":
            lc_loss *= .25
            s.cash_m -= 1.2
        elif action == "diversify":
            freight_cost *= .55
            delay_loss *= .75
            s.cash_m -= .8
        elif action == "working_capital":
            inventory_cost *= .45
            s.cash_m -= 1.0
            s.ccc_days -= 2
        elif action == "reprice":
            s.yield_rate += .0015
            s.npl_ratio += .001
        elif action == "monitor":
            s.risk_score = max(0, s.risk_score - 2)
        gross_loss = max(0, freight_cost + delay_loss + inventory_cost + lc_loss + claim_loss)
        s.portfolio_m = max(0, s.portfolio_m - gross_loss)
        s.cash_m = max(0, s.cash_m + s.portfolio_m * s.yield_rate / 52 - gross_loss*.08)
        s.ccc_days += scenario["inventory_days"]*.35 + scenario["delay_days"]*.15
        s.risk_score = min(100, s.risk_score + scenario["severity"]*2 - (3 if action != "monitor" else 1))
        s.supply_chain_usage += 1 if action in ["diversify", "monitor", "working_capital"] else .5
        s.decisions += 1
        s.history.append({"week":s.week, "scenario":scenario["name"], "action":action,
                          "financial_impact_m":round(gross_loss,3), "ccc_days":round(s.ccc_days,1)})
        s.week += 1
        return {"scenario":scenario, "gross_loss_m":gross_loss, "freight_cost_m":freight_cost,
                "delay_loss_m":delay_loss, "inventory_cost_m":inventory_cost,
                "lc_expiry_loss_m":lc_loss, "insurance_loss_m":claim_loss, "state":s}

    def score(self):
        s = self.state
        financial = max(0, min(300, 300 * (s.portfolio_m / 500) * min(1.2, s.yield_rate/.02)))
        risk = max(0, min(250, 250 * (1 - s.risk_score/120) * (1 - min(.8,s.npl_ratio))))
        intelligence = min(200, 40 + 12*s.supply_chain_usage)
        speed = min(100, 100 if s.decisions else 0)
        learning = min(150, 75 + max(0, s.week-1)*2)
        return {"financial_performance":round(financial), "risk_management":round(risk),
                "supply_chain_intelligence":round(intelligence), "decision_speed":round(speed),
                "learning_progression":round(learning),
                "total":round(financial+risk+intelligence+speed+learning)}
