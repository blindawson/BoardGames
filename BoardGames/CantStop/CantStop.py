import pandas as pd
import numpy as np
from itertools import combinations


def dice_df():
    df = pd.DataFrame(
        np.array(
            np.meshgrid(range(1,7), range(1,7),
                        range(1,7), range(1,7)))
        .reshape(4, -1).T,
        columns=['D1', 'D2', 'D3', 'D4'])
    df['D12'] = df['D1'] + df['D2']
    df['D13'] = df['D1'] + df['D3']
    df['D14'] = df['D1'] + df['D4']
    df['D23'] = df['D2'] + df['D3']
    df['D24'] = df['D2'] + df['D4']
    df['D34'] = df['D3'] + df['D4']
    return df


def odds(n1, n2, n3):
    dice = dice_df()
    hits = pd.DataFrame([])
    hits['n1'] = (dice.loc[:, 'D12':'D34'] == n1).any(axis=1)
    hits['n2'] = (dice.loc[:, 'D12':'D34'] == n2).any(axis=1)
    hits['n3'] = (dice.loc[:, 'D12':'D34'] == n3).any(axis=1)
    hits['any'] = hits.loc[:,'n1':'n3'].any(axis=1)
    return hits['any'].sum() / len(hits)


def odds_table():
    df = pd.DataFrame(list(combinations(range(2,13), 3)),
                      columns=['N1', 'N2', 'N3'])
    df['Odds'] = df.apply(lambda r: odds(r['N1'], r['N2'], r['N3']), axis=1)
    return df


# How much is there to gain by hitting on one or two of three numbers.
def benefit():
