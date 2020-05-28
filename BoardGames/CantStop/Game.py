import pandas as pd
import numpy as np
import sys
from itertools import combinations, groupby
from BoardGames.CantStop import Components
from BoardGames.CantStop import Player

# The game holds the rules of the game and turn progression.


class Game:
    def __init__(self, *args):
        self.players = []
        self.dice = Components.Dice()
        if len(args) == 0:
            args = ('P1', 'P2')
        for player in args:
            if isinstance(player, str):
                self.players.append(Player.Player(player))
            elif isinstance(player, Player):
                self.players.append(player)
        self.board = Components.Board(args)
        self.starting_player = np.random.choice(self.players)
        self.active_player = self.starting_player
        self.start_turn(self.starting_player)

    def start_turn(self, player):
        self.active_player = player
        self.print_status()
        option = str(input('Continue Game? [y/n]'))
        if option == 'y':
            self.roll_dice()

    def roll_dice(self):
        self.dice = self.dice.roll_dice()
        print(f'{self.active_player.name} rolled: {self.dice}')
        self.check_dice()

    def check_dice(self):
        def remove_unusable_dice_sums(board, pair):
            for p in pair:
                if board.df.loc[p, 'Locked']:
                    pair.remove(p)
            if board.available_runners() >= 2:
                pass
            elif board.available_runners() == 1:
                if any(x in board.active_runner_cols() for x in pair):
                    pass
                else:
                    pair = pair[0], pair[1]
            elif board.available_runners() == 0:
                for p in pair:
                    if p not in board.active_runner_cols():
                        pair.remove(p)
            return pair

        def clean_list(list_):
            for elem in list_:
                # split tuple into individual entries
                if type(elem) == tuple:
                    list_.insert(len(list_), elem[0])
                    list_.insert(len(list_), elem[1])
                    list_.remove(elem)
                # remove empty entries
                elif not elem:
                    list_.remove(elem)
            # ascending order
            for i, elem in enumerate(list_):
                if type(elem) == list:
                    list_[i] = sorted(elem)
            # remove duplicates
            list_.sort()
            list_ = list(x for x, _ in groupby(list_))
            return list_

        pairs = list(map(lambda x: remove_unusable_dice_sums(self.board, x), self.dice.pair()))
        pairs = clean_list(pairs)
        if not pairs:
            self.bust()
        else:
            self.choose_dice(pairs)

    def choose_dice(self, pairs):
        print(f'Your options are:')
        for i, p in enumerate(pairs):
            if len(p) == 2:
                print(f'{i+1}: Move {p[0]} and {p[1]}')
            else:
                print(f'{i+1}: Move {p[0]}')
        option = int(input('Choose option:')) - 1
        if option not in range(len(pairs)):
            print(f'You Chose {option}. Please choose 1-{len(pairs)}.')
            self.choose_dice(pairs)
        else:
            selected_cols = pairs[option]
            self.board.advance_runners(self.active_player, selected_cols)
            self.print_status()
            self.ask_continue()

    def ask_continue(self):
        option = str(input('Roll again? [y/n]'))
        if option == 'y':
            print("Can't Stop!\n")
            self.roll_dice()
        if option == 'n':
            print("Chicken!\n")
            self.board.lock_runner_progress(self.active_player)
            self.end_turn()
        else:
            pass

    def end_turn(self):
        self.board.reset_runners()
        self.check_score()
        self.start_turn(self.next_player())

    def check_score(self):
        for i in range(len(self.players)):
            self.players[i].score = (self.board.df.loc[:, self.players[i].name] ==
                                     self.board.df.loc[:, 'Column Height']).sum()
        if any(p.score >= 3 for p in self.players):
            print(f'{self.active_player} Wins!!!')
            sys.exit('Game Over')

    def next_player(self):
        index = self.players.index(self.active_player) + 1
        if index == len(self.players):
            index = 0
        self.active_player = self.players[index]
        return self.active_player

    def bust(self):
        print('YOU BUUUUUUUSTED!\n')
        self.end_turn()

    def print_status(self):
        print(f"{self.active_player.name}'s Turn")
        print(self.board.df.iloc[:, :-1].T)

    # TODO Check that Num players is 2 to 4
    # TODO Choose first player
    # TODO Make a turn class and have the first player take their turn
    # TODO Alternate Players Turn
    # TODO Check end of turn
    # TODO Dice pair verbose should default to false


def odds(*args):
    hits = pd.DataFrame([])
    for i, num in enumerate(args):
        hits[i] = (Components.Dice.all_dice_combinations().loc[:, 'D01':'D12'] == num).any(axis=1)
    hits['any'] = hits.loc[:, 0:len(args)].any(axis=1)
    return hits['any'].sum() / len(hits)


def odds_table():
    df = pd.DataFrame(list(combinations(range(2, 13), 3)),
                      columns=['N1', 'N2', 'N3'])
    df['Odds'] = df.apply(lambda r: odds(r['N1'], r['N2'], r['N3']), axis=1)
    return df


def progress_value(row, position=0):
    total_spaces = Components.Board().col_len[row]
    remaining_spaces = total_spaces - position
    if remaining_spaces == 0:
        return 0
    else:
        return 1 / remaining_spaces


# TODO turn counter
