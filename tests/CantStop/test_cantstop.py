import pandas as pd
import pytest
from BoardGames.CantStop import *

odds_table = pd.read_csv('odds_table.csv', header=0, index_col=0)
dice_df = pd.read_csv('dice_df.csv', header=0, index_col=0)


def test_dice_class():
    dice = Components.Dice(1, 2, 5, 6)
    assert dice.values[0] == 1
    assert dice.values[1] == 2
    assert dice.values[2] == 5
    assert dice.values[3] == 6


def test_board_class():
    board = Components.Board('p1', 'p2', 'p3', 'p4')
    assert board.col_len[9] == 9


def test_pair_dice():
    dice = Components.Dice(1, 2, 5, 6)
    assert dice.pair() == [[3, 11], [6, 8], [7, 7]]


def test_all_dice_combinations():
    assert Components.all_dice_combinations().values == pytest.approx(dice_df.values)


def test_odds_table():
    assert Game.odds_table().values == pytest.approx(odds_table.values)


def test_progress_value():
    assert Game.progress_value(3, 1) == 0.25
    assert Game.progress_value(8, 5) == 1 / 6
    assert Game.progress_value(11, 0) == 1 / 5
    assert Game.progress_value(12, 3) == 0


# def test_game_init():
#     assert CantStop.Game('p1', 'p2', 'p3').players == [CantStop.Player('p1'),
#                                                        CantStop.Player('p2'),
#                                                        CantStop.Player('p3')]


def test_odds():
    assert Game.odds(6, 7, 8) == 0.9197530864197531
    assert Game.odds(2, 4, 5) == 0.6574074074074074
    assert Game.odds(9, 3, 8) == 0.8356481481481481

# def test_choose_rows():
#     assert CantStop.choose_rows(d1=1, d2=2, d3=3, d4=4) ==
#     assert CantStop.choose_rows(d1=5, d2=3, d3)

# TODO Some tests like test_all_dice_combinations prints a ton to the output.
#  Where is that coming from and how do I remove it?


def test_advance_runner():
    runners = [Components.Runner(), Components.Runner(), Components.Runner()]
    runners[1].column = 7
    runners[1].height = 3
    runners = Components.Runner.advance_runner(runners, 7)
    assert runners[1].height == 4
    runners = Components.Runner.advance_runner(runners, 2)
    assert runners[0].column == 2
    assert runners[0].height == 1
