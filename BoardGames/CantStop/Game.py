import pandas as pd
import numpy as np
from itertools import combinations
from BoardGames.CantStop import Components
from BoardGames.CantStop import Player

# The game holds the rules of the game and turn progression.


class Game:
    def __init__(self, *args):
        self.board = Components(args)
        self.players = []
        self.dice = Components.Dice()
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
            self.roll_dice()

    def roll_dice(self):
        self.dice = self.dice.roll_dice()
        print(f'{self.active_player.name} rolled: {self.dice}')
        self.check_dice()

    def check_dice(self):
        pairs = self.dice.pair()
        use_pairs = list(map(lambda x: self.check_dice_pairing(x), self.pairs))
        if all(x == 'NN' for x in use_pairs):
            self.Bust()
        else:
            self.choose_dice(use_pairs)

    def check_dice_pairing(self, pair):
        runners = self.active_player.runners
        available_runners = sum(self.board.available_runners())
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

    @staticmethod
    def list_progress_options(self, pair, use_pair, option_dict):
        n = len(option_dict)
        if use_pair == 'YY':
            option_dict.update({n + 1: pair})
            print(f'{n + 1}: Move {pair[0]} and {pair[1]}')
        elif use_pair == 'YN':
            option_dict.update({n + 1: [pair[0]]})
            print(f'{n + 1}: Move {pair[0]}')
        elif use_pair == 'NY':
            option_dict.update({n + 1: [pair[1]]})
            print(f'{n + 1}: Move {pair[1]}')
        elif use_pair == 'YorY':
            option_dict.update({n + 1: [pair[0]], n + 2: [pair[1]]})
            print(f'{n + 1}: Move {pair[0]}\n'
                  f'{n + 2}: Move {pair[1]}')
        return option_dict

    def choose_dice(self, use_pairs):
        print(f'Your options are:')
        option_dict = {}
        for pair, use_pair in zip(self.dice.pair(), use_pairs):
            option_dict = self.list_progress_options(pair, use_pair, option_dict)
        option = int(input('Choose option:'))
        if option not in range(1, len(option_dict) + 1):
            print(f'You Chose {option}. Please choose 1-{len(option_dict)}.')
            self.choose_dice(use_pairs)
        else:
            self.active_player.climb_columns(option_dict(option))
            print(self.active_player.columns.to_frame().T)
            self.ask_continue()

    def ask_continue(self):
        option = str(input('Continue [y/n]?'))
        if option == 'y':
            print("Can't Stop!")
            self.roll_dice()
        if option == 'n':
            print("Chicken!")
            self.lock_in_progress()
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

    def bust(self):
        self.end_turn()
        pass

    # TODO
    def lock_in_progress(self):
        # Player progress gets updated to height of each in-use runner

        pass

    # TODO Check that Num players is 2 to 4
    # TODO Choose first player
    # TODO Make a turn class and have the first player take their turn
    # TODO Alternate Players Turn
    # TODO Check end of turn
    # TODO Dice pair verbose should default to false


def odds(*args):
    hits = pd.DataFrame([])
    for i, num in enumerate(args):
        hits[i] = (Components.all_dice_combinations().loc[:, 'D01':'D12'] == num).any(axis=1)
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
# TODO bust

