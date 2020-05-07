import pandas as pd
import numpy as np
from itertools import combinations


class Dice:
    def __init__(self, d1=None, d2=None, d3=None, d4=None):
        self.values = pd.Series([d1, d2, d3, d4])

        def set_rand(d):
            if d is None:
                d = np.random.randint(1, 7)
            return d
        self.values = self.values.apply(lambda d: set_rand(d))

    def __repr__(self):
        return f'{self.values[0]}, {self.values[1]}, {self.values[2]}, {self.values[3]}'

    def roll_dice(self):
        self.values = self.values.apply(lambda d: np.random.randint(1, 7))
        return self

    def pair(self, verbose=False):
        d01 = self.values[0] + self.values[1]
        d02 = self.values[0] + self.values[2]
        d03 = self.values[0] + self.values[3]
        d12 = self.values[1] + self.values[2]
        d13 = self.values[1] + self.values[3]
        d23 = self.values[2] + self.values[3]
        # TODO Would be nice to print lowest to highest
        if verbose:
            print(f'{d01} and {d23}\n'
                  f'{d02} and {d13}\n'
                  f'{d03} and {d12}')
        return [[d01, d23], [d02, d13], [d03, d12]]


class Board:
    def __init__(self, *args):
        if len(args) == 0:
            args = ('p1', 'p2')
        self.col_len = pd.Series([3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3],
                                 index=range(2, 13), name='Column Length')
        self.df = pd.DataFrame(0, index=self.col_len.index, columns=list(args[0]))
        self.df.index.name = 'Column Number'
        self.df['Column Length'] = self.col_len
        self.df['Locked'] = False

    def move_runner(self, player, column_number):
        if self.df.loc[column_number, player] == self.df.loc[column_number, 'Column Length']:
            raise Exception('Runner cannot move any higher.')
        self.df.loc[column_number, player] += 1
        player.columns[column_number] += 1

    def lock_column(self, column_number):
        if self.df.loc[column_number, 'Locked']:
            raise Exception('Column is already locked.')
        self.df.loc[column_number, 'Locked'] = True

    # TODO add __repr__. It'd be extra cool if this could be a figure


class Player:
    def __init__(self, name='Anonymous'):
        self.score = 0
        self.columns = pd.Series(0, index=range(2, 13), name='Column Progress')
        self.name = name

    def __repr__(self):
        return (f'{self.name}\n'
                f'Score: {self.score}\n'
                f'{self.columns.to_frame().T}')


class Turn:
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.dice = Dice()
        self.start_turn()

    def start_turn(self):
        print(f"{self.player.name}'s Turn")
        self.roll()

    def roll(self):
        self.dice = self.dice.roll_dice()
        print(f'{self.player.name} rolled: {self.dice}')
        self.resolve_roll()

    def resolve_roll(self):
        self.choose_dice()

    def choose_dice(self):
        print(f'Your options are:')
        self.dice.pair(verbose=True)
        option = int(input('Choose pair 1, 2, or 3:'))
        if option not in [1, 2, 3]:
            print(f'You Chose {option}. Please choose 1, 2, or 3.')
            self.choose_dice()
        else:
            self.player.columns[self.dice.pair()[option - 1][0]] += 1
            self.player.columns[self.dice.pair()[option - 1][1]] += 1
            print(self.player.columns.to_frame().T)
            self.ask_continue()

    def ask_continue(self):
        option = str(input('Continue [y/n]?'))
        if option == 'y':
            self.roll()


class Game:
    def __init__(self, *args):
        self.board = Board(args)
        self.players = []
        for player in args:
            if isinstance(player, str):
                self.players.append(Player(player))
            elif isinstance(player, Player):
                self.players.append(player)
        if len(args) == 0:
            self.players.append(Player('P1'))
            self.players.append(Player('P2'))
        self.starting_player = np.random.choice(self.players)
        Turn(self.starting_player, self.board)

    def turn(self, player):
        Turn(player, self.board)

    # TODO Check that Num players is 2 to 4
    # TODO Choose first player
    # TODO Make a turn class and have the first player take their turn
    # TODO Alternate Players Turn
    # TODO Check end of turn
    # TODO Dice pair verbose should default to false


def all_dice_combinations():
    df = pd.DataFrame(
        np.array(
            np.meshgrid(range(1, 7), range(1, 7),
                        range(1, 7), range(1, 7)))
        .reshape(4, -1).T,
        columns=['D0', 'D1', 'D2', 'D3'])
    df['D01'] = df['D0'] + df['D1']
    df['D23'] = df['D2'] + df['D3']
    df['D02'] = df['D0'] + df['D2']
    df['D13'] = df['D1'] + df['D3']
    df['D03'] = df['D0'] + df['D3']
    df['D12'] = df['D1'] + df['D2']
    return df


def odds(*args):
    hits = pd.DataFrame([])
    for i, num in enumerate(args):
        hits[i] = (all_dice_combinations().loc[:, 'D01':'D12'] == num).any(axis=1)
    hits['any'] = hits.loc[:, 0:len(args)].any(axis=1)
    return hits['any'].sum() / len(hits)


def odds_table():
    df = pd.DataFrame(list(combinations(range(2, 13), 3)),
                      columns=['N1', 'N2', 'N3'])
    df['Odds'] = df.apply(lambda r: odds(r['N1'], r['N2'], r['N3']), axis=1)
    return df


def progress_value(row, position=0):
    total_spaces = Board().col_len[row]
    remaining_spaces = total_spaces - position
    if remaining_spaces == 0:
        return 0
    else:
        return 1 / remaining_spaces




# TODO turn counter
# TODO bust

