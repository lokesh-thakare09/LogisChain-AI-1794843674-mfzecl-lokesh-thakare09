from src.finance.risk import expected_loss, cash_conversion_cycle, supply_chain_adjusted_pd

def test_expected_loss():
    assert expected_loss(.02, .4, 1000) == 8

def test_ccc():
    assert cash_conversion_cycle(50, 40, 30) == 60

def test_pd_is_probability():
    p = supply_chain_adjusted_pd(.03, .9, 4, 2, .2)
    assert 0 < p < 1
