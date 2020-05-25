import pandas as pd

# The player holds the player name, and their progress on each column


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

    def climb_columns(self, cols):
        # for each c in cols
        # If a runner is already on that col then move it up
        # else grab a new runner and move it up from wherever that player has progressed to on that column
        pass
