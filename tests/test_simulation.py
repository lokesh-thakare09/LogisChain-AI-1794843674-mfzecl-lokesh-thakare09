from src.simulation.engine import SimulationEngine
from src.simulation.scenarios import SCENARIOS

def test_scenario_catalogue():
    assert len(SCENARIOS) >= 10

def test_simulation_network_and_turn():
    e = SimulationEngine()
    info = e.network_info()
    assert info["nodes"] >= 100
    assert info["edges"] >= 500
    out = e.apply_week(0, "monitor")
    assert out["gross_loss_m"] >= 0
    assert e.state.week == 2

def test_game_modes():
    e = SimulationEngine()
    e.new_game("Supply Chain Finance Pricing")
    assert e.state.mode == "Supply Chain Finance Pricing"
