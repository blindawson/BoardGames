import pandas as pd
import numpy as np
from itertools import combinations
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
        def check_dice_pairing(board, pair):
            if board.available_runners() >= 2:
                use_pair = 'YY'
            elif board.available_runners() == 1:
                if any(x in board.active_runner_cols() for x in pair):
                    use_pair = 'YY'
                else:
                    use_pair = 'YorY'
            else:
                if all(x in board.active_runner_cols() for x in pair):
                    use_pair = 'YY'
                elif pair[0] in board.active_runner_cols():
                    use_pair = 'YN'
                elif pair[1] in board.active_runner_cols():
                    use_pair = 'NY'
                else:
                    use_pair = 'NN'
            return use_pair

        pairs = self.dice.pair()
        use_pairs = list(map(lambda x: check_dice_pairing(self.board, x), pairs))
        if all(x == 'NN' for x in use_pairs):
            self.bust()
        else:
            self.choose_dice(use_pairs)

    @staticmethod
    def list_dice_choices(pair, use_pair, option_dict):
        def is_duplicate(x):
            if (x in option_dict.values()) or (x[::-1] in option_dict.values()):
                return True
            else:
                return False

        n = len(option_dict)
        if use_pair == 'YY':
            if not is_duplicate(pair):
                option_dict.update({n + 1: pair})
                print(f'{n + 1}: Move {pair[0]} and {pair[1]}')
        elif use_pair == 'YN':
            if not is_duplicate([pair[0]]):
                option_dict.update({n + 1: [pair[0]]})
                print(f'{n + 1}: Move {pair[0]}')
        elif use_pair == 'NY':
            if not is_duplicate([pair[1]]):
                option_dict.update({n + 1: [pair[1]]})
                print(f'{n + 1}: Move {pair[1]}')
        elif use_pair == 'YorY':
            if not is_duplicate([pair[0]]):
                option_dict.update({n + 1: [pair[0]]})
                print(f'{n + 1}: Move {pair[0]}')
                n += 1
            if not is_duplicate([pair[1]]):
                option_dict.update({n + 1: [pair[1]]})
                print(f'{n + 1}: Move {pair[1]}')
        return option_dict

    def choose_dice(self, use_pairs):
        print(f'Your options are:')
        option_dict = {}
        for pair, use_pair in zip(self.dice.pair(), use_pairs):
            option_dict = self.list_dice_choices(pair, use_pair, option_dict)
        option = int(input('Choose option:'))
        if option not in range(1, len(option_dict) + 1):
            print(f'You Chose {option}. Please choose 1-{len(option_dict)}.')
            self.choose_dice(use_pairs)
        else:
            selected_cols = option_dict[option]
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
            self.board.lock_in_progress(self.active_player)
            self.end_turn()
        else:
            pass

    def end_turn(self):
        self.board.reset_runners()
        self.board.df['Runners'] = 0
        self.start_turn(self.next_player())

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
