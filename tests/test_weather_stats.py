import pytest
from src.utils.weather_stats import TemperatureProcessor

def test_get_average():
    tp = TemperatureProcessor([10, 20, 30])
    assert tp.get_average() == 20.0

def test_get_extremes():
    tp = TemperatureProcessor([10, 20, 30])
    assert tp.get_extremes() == (10, 30)

def test_get_average_empty_list():
    with pytest.raises(ValueError):
        tp = TemperatureProcessor([])
        tp.get_average()

def test_get_extremes_empty_list():
    with pytest.raises(ValueError):
        tp = TemperatureProcessor([])
        tp.get_extremes()
