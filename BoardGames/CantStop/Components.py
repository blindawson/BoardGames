import pandas as pd
import numpy as np


class Board:
    def __init__(self, players):
        self.col_len = pd.Series([3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3],
                                 index=range(2, 13), name='Column Height')
        self.df = pd.DataFrame(0, index=self.col_len.index, columns=['Runners'] + list(players))
        self.df.index.name = 'Column'
        self.df['Column Height'] = self.col_len
        self.df['Locked'] = False
        self.runners = [Runner(), Runner(), Runner()]

    def lock_column(self, column_number):
        if self.df.loc[column_number, 'Locked']:
            raise Exception('Column is already locked.')
        self.df.loc[column_number, 'Locked'] = True

    def reset_runners(self):
        self.runners = [Runner(), Runner(), Runner()]

    def advance_runners(self, columns, height=1):
        for c in columns:
            if self.runners[0].column == c:
                self.runners[0].advance()
            elif self.runners[1].column == c:
                self.runners[1].advance()
            elif self.runners[2].column == c:
                self.runners[2].advance()
            else:
                i = [x.available() for x in self.runners].index(True)
                self.runners[i].place_runner(c, height)
        active_runners = list(filter(lambda x: x.column != 0, self.runners))
        runner_cols = [x.column for x in active_runners]
        runner_heights = [x.height for x in active_runners]
        self.df.loc[runner_cols, 'Runners'] = runner_heights

    def lock_in_progress(self, player):
        self.df.loc[:, player.name] = self.df.loc[:, ['Runners', player.name]].max(axis=1)

    # TODO add __repr__. It'd be extra cool if this could be a figure


class Runner:
    def __init__(self):
        self.column = 0
        self.height = 0

    def place_runner(self, col, height):
        self.column = col
        self.height = height

    def advance(self):
        self.height += 1

    def available(self):
        if self.column == 0:
            return True
        else:
            return False

    def active(self):
        return not self.available()


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
