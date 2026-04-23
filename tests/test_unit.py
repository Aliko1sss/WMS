import pytest
from app.operations import calculate_stock

def test_incoming_calculation():
    assert calculate_stock(10.0, "IN", 5.0) == 15.0

def test_outgoing_calculation():
    assert calculate_stock(10.0, "OUT", 3.0) == 7.0

def test_negative_amount_error():
    with pytest.raises(ValueError, match="> 0"):
        calculate_stock(10.0, "IN", -1.0)