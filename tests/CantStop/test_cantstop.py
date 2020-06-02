import pandas as pd
import pytest
import pickle
from BoardGames.CantStop import *

odds_table = pd.read_csv('odds_table.csv', header=0, index_col=0)
dice_df = pd.read_csv('dice_df.csv', header=0, index_col=0)


def test_dice_class():
    dice = Components.Dice([1, 2, 5, 6])
    assert dice.values[0] == 1
    assert dice.values[1] == 2
    assert dice.values[2] == 5
    assert dice.values[3] == 6


def test_board_class():
    board = Components.Board(players=['p1', 'p2', 'p3', 'p4'])
    assert board.col_len[9] == 9


def test_pair_dice():
    dice = Components.Dice([1, 2, 5, 6])
    assert dice.pair() == [[3, 11], [6, 8], [7, 7]]


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


def test_edge_case01(mocker):
    user_inputs = ['q', [1, 1, 6, 4], 1,
                   'q', [6, 4, 6, 6], 1,
                   'q', [5, 5, 2, 2], 99]
    mocker.patch('builtins.input', side_effect=user_inputs)
    game = Game.Game()
    assert game.pairs == [[10]]


def test_edge_case02(mocker):
    user_inputs = ['q', [3, 3, 6, 4], 1,
                   'q', [5, 5, 2, 4], 99]
    mocker.patch('builtins.input', side_effect=user_inputs)
    game = Game.Game()
    assert all(game.board.active_runner_cols() == [6, 10])


def test_edge_case03(mocker):
    user_inputs = ['q', [6, 6, 4, 1], 1,
                   'q', [6, 4, 1, 2], 1,
                   'q', [2, 6, 1, 2], 1, 'n',
                   'q', [3, 5, 5, 5], 1,
                   'q', [6, 6, 4, 1], 99]
    mocker.patch('builtins.input', side_effect=user_inputs)
    game = Game.Game()
    assert all(game.board.active_runner_cols() == [8, 10])


def test_edge_case04(mocker):
    state = pickle.load(open('logs/rand_state04.p', 'rb'))
    user_inputs = ['y', 1, 'y', 1, 'n',
                   'y', 1, 'y', 99]
    mocker.patch('builtins.input', side_effect=user_inputs)
    Game.Game(random_state=state)
    assert 1 == 1


def test_edge_case05(mocker):
    state = pickle.load(open('logs/rand_state05.p', 'rb'))
    user_inputs = pickle.load(open('logs/user_inputs05.p', 'rb')) + ['n', 'n']
    mocker.patch('builtins.input', side_effect=user_inputs)
    Game.Game(random_state=state)
    assert 1 == 1


# Odds Tests
def test_all_dice_combinations():
    assert Components.Dice.all_dice_combinations().values == pytest.approx(dice_df.values)


def test_odds_table():
    assert Game.odds_table().values == pytest.approx(odds_table.values)