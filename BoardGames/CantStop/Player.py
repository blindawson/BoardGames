import pandas as pd

# The player holds the player name, and their progress on each column


class Player:
    def __init__(self, name='Anonymous'):
        self.score = 0
        self.columns = pd.DataFrame(0, index=range(2, 13), columns=['Runner Progress', 'Permanent Progress'])
        self.name = name
        self.runners = []

    def __repr__(self):
        return (f'{self.name}\n'
                f'Score: {self.score}\n'
                f'{self.columns.T}')

    def climb_columns(self, cols):
        for c in cols:
            self.columns.loc[c, 'Runner Progress'] = self.columns.loc[c, :].max() + 1
        pass
