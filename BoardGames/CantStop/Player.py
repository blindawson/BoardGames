import pandas as pd


class Player:
    def __init__(self, name='Anonymous'):
        self.score = 0
        self.columns = pd.Series(0, index=range(2, 13), name='Column Progress')
        self.name = name

    def __repr__(self):
        return (f'{self.name}\n'
                f'Score: {self.score}\n'
                f'{self.columns.to_frame().T}')