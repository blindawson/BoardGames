import pandas as pd

# The player holds the player name and total score


class Player:
    def __init__(self, name='Anonymous'):
        self.score = 0
        self.name = name

    def __repr__(self):
        return (f'{self.name}\n'
                f'Score: {self.score}\n')
