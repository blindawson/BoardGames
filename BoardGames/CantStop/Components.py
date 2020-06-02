import pandas as pd
import numpy as np


class Board:
    def __init__(self, players=None):
        if players is None:
            players = ['P1', 'P2']
        self.col_len = pd.Series([3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3],
                                 index=range(2, 13), name='Column Height')
        self.df = pd.DataFrame(0, index=self.col_len.index, columns=['Runners'] + list(players))
        self.df.index.name = 'Column'
        self.df['Column Height'] = self.col_len
        self.df['Locked'] = False

    def lock_column(self, column_number):
        if self.df.loc[column_number, 'Locked']:
            raise Exception('Column is already locked.')
        self.df.loc[column_number, 'Locked'] = True

    def reset_runners(self):
        self.df['Runners'] = 0

    def advance_runners(self, player, columns):
        for c in columns:
            self.df.loc[c, 'Runners'] = self.df.loc[c, [player.name, 'Runners']].max() + 1

    def available_runners(self):
        return 3 - (self.df['Runners'] > 0).sum()

    def active_runner_cols(self):
        return self.df[self.df['Runners'] > 0].index.values

    def lock_runner_progress(self, player):
        self.df.loc[:, player.name] = self.df.loc[:, ['Runners', player.name]].max(axis=1)
        completed_cols = (self.df.loc[:, player.name] == self.df.loc[:, 'Column Height'])
        self.df.loc[completed_cols, 'Locked'] = True

    # TODO add __repr__. It'd be extra cool if this could be a figure


class Dice:
    def __init__(self, faces=None):
        # TODO does this need to be a pandas series?
        if faces is None:
            self.values = list(np.random.randint(1, 7, 4))
        else:
            self.values = faces

    def __repr__(self):
        return f'{self.values[0]}, {self.values[1]}, {self.values[2]}, {self.values[3]}'

    def roll_dice(self, roll_result=None):
        if roll_result is None:
            self.values = list(map(int, np.random.randint(1, 7, 4)))
        else:
            self.values = roll_result
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

    @staticmethod
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
