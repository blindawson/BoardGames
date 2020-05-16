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
        self.runners = []

    def __repr__(self):
        return (f'{self.name}\n'
                f'Score: {self.score}\n'
                f'{self.columns.to_frame().T}')


class Game:
    def __init__(self, *args):
        self.board = Board(args)
        self.players = []
        self.dice = Dice()
        for player in args:
            if isinstance(player, str):
                self.players.append(Player(player))
            elif isinstance(player, Player):
                self.players.append(player)
        if len(args) == 0:
            self.players.append(Player('P1'))
            self.players.append(Player('P2'))
        self.starting_player = np.random.choice(self.players)
        self.active_player = self.starting_player
        self.start_turn(self.starting_player)

    def start_turn(self, player):
        self.active_player = player
        option = str(input('Play Game [y/n]?'))
        if option == 'y':
            print(f"{player.name}'s Turn")
            self.roll()

    def roll(self):
        self.dice = self.dice.roll_dice()
        print(f'{self.active_player.name} rolled: {self.dice}')
        self.resolve_roll(self.dice)

    def resolve_roll(self, dice):
        pairs = dice.pair()
        use_pair1 = self.check_pair(pairs[0])
        use_pair2 = self.check_pair(pairs[1])
        use_pair3 = self.check_pair(pairs[2])
        self.choose_dice([use_pair1, use_pair2, use_pair3])

    def check_pair(self, pair):
        runners = self.active_player.runners
        available_runners = 3 - len(runners)
        if available_runners >= 2:
            use_pair = 'YY'
        elif available_runners == 1:
            if any(x in runners for x in pair):
                use_pair = 'YY'
            else:
                use_pair = 'YorY'
        else:
            if all(x in runners for x in pair):
                use_pair = 'YY'
            elif pair[0] in runners:
                use_pair = 'YN'
            elif pair[1] in runners:
                use_pair = 'NY'
            else:
                use_pair = 'NN'
        return use_pair

    def column_options(self, pair, use_pair, option_dict):
        n = len(option_dict)
        if use_pair == 'YY':
            option_dict.update({n+1: pair})
            print(f'{n+1}: Move {pair[0]} and {pair[1]}')
        elif use_pair == 'YN':
            option_dict.update({n+1: [pair[0]]})
            print(f'{n+1}: Move {pair[0]}')
        elif use_pair == 'NY':
            option_dict.update({n+1: [pair[1]]})
            print(f'{n+1}: Move {pair[1]}')
        if use_pair == 'YorY':
            option_dict.update({n+1: [pair[0]], n+2: [pair[1]]})
            print(f'{n+1}: Move {pair[0]}\n'
                  f'{n+2}: Move {pair[1]}')
        return option_dict

    def choose_dice(self, use_pairs):
        print(f'Your options are:')
        option_dict = {}
        for pair, use_pair in zip(self.dice.pair(), use_pairs):
            option_dict = self.column_options(pair, use_pair, option_dict)
        option = int(input('Choose option:'))
        if option not in range(1, len(option_dict)+1):
            print(f'You Chose {option}. Please choose 1-{len(option_dict)}.')
            self.choose_dice(use_pairs)
        else:
            self.active_player.columns[self.dice.pair()[option - 1][0]] += 1
            self.active_player.columns[self.dice.pair()[option - 1][1]] += 1
            print(self.active_player.columns.to_frame().T)
            self.ask_continue()

    def ask_continue(self):
        option = str(input('Continue [y/n]?'))
        if option == 'y':
            print("Can't Stop!")
            self.roll()
        if option == 'n':
            print("Chicken!")
            self.end_turn()
        else:
            pass

    def end_turn(self):
        self.start_turn(self.next_player())

    def next_player(self):
        index = self.players.index(self.active_player) + 1
        if index == len(self.players):
            index = 0
        self.active_player = self.players[index]
        return self.active_player

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

