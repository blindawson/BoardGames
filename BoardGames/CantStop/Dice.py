import pandas as pd
import numpy as np


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