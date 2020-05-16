import pandas as pd
import numpy as np
from itertools import combinations
from BoardGames.CantStop import Board
from BoardGames.CantStop import Player
from BoardGames.CantStop import Dice


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
        print(f"{player.name}'s Turn")
        self.roll()

    def roll(self):
        self.dice = self.dice.roll_dice()
        print(f'{self.active_player.name} rolled: {self.dice}')
        self.resolve_roll()

    def resolve_roll(self):
        self.check_dice()
        self.choose_dice()

    def choose_dice(self):
        print(f'Your options are:')
        self.dice.pair(verbose=True)
        option = int(input('Choose pair 1, 2, or 3:'))
        if option not in [1, 2, 3]:
            print(f'You Chose {option}. Please choose 1, 2, or 3.')
            self.choose_dice()
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


def odds(*args):
    hits = pd.DataFrame([])
    for i, num in enumerate(args):
        hits[i] = (Dice.all_dice_combinations().loc[:, 'D01':'D12'] == num).any(axis=1)
    hits['any'] = hits.loc[:, 0:len(args)].any(axis=1)
    return hits['any'].sum() / len(hits)


def odds_table():
    df = pd.DataFrame(list(combinations(range(2, 13), 3)),
                      columns=['N1', 'N2', 'N3'])
    df['Odds'] = df.apply(lambda r: odds(r['N1'], r['N2'], r['N3']), axis=1)
    return df


def progress_value(row, position=0):
    total_spaces = Board.Board().col_len[row]
    remaining_spaces = total_spaces - position
    if remaining_spaces == 0:
        return 0
    else:
        return 1 / remaining_spaces

def check_pair(pair):


# TODO turn counter
# TODO bust

