import pandas as pd


class Board:
    def __init__(self, *players):
        if len(players) == 0:
            players = ('p1', 'p2')
        self.col_len = pd.Series([3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3],
                                 index=range(2, 13), name='Column Length')
        self.df = pd.DataFrame(0, index=self.col_len.index, columns=list(players))
        self.df.index.name = 'Column Number'
        self.df['Column Length'] = self.col_len
        self.df['Locked'] = False
        self.runners = [0, 0, 0]

    def available_runners(self):
        return self.runners.count(0)

    def next_runner(self):
        try:
            return self.runners.index(0)
        except ValueError:
            raise Exception('No runners available.')

    def move_runner(self, player, column_number):
        if self.df.loc[column_number, player] == self.df.loc[column_number, 'Column Length']:
            raise Exception('Runner cannot move any higher.')
        self.df.loc[column_number, player] += 1
        player.columns[column_number] += 1
        if column_number not in self.runners:
            self.runners[self.next_runner()] = column_number

    def lock_column(self, column_number):
        if self.df.loc[column_number, 'Locked']:
            raise Exception('Column is already locked.')
        self.df.loc[column_number, 'Locked'] = True

    # TODO add __repr__. It'd be extra cool if this could be a figure
