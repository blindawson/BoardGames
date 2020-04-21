import pandas as pd
import pathlib
import pytest
from BoardGames.CantStop import CantStop


def test_peak_outputs():
    odds_table = pd.read_csv('odds_table.csv', header=0, index_col=0)
    assert CantStop.odds_table().values == pytest.approx(odds_table.values)
