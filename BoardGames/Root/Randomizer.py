import random
import pandas as pd

all_factions = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond',
                'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult']
reach = {'Marquise de Cat': 10,
         'Eyrie Dynasties': 7,
         'Vagabond': 5,
         'Riverfolk Company': 5,
         'Woodland Alliance': 3,
         'Lizard Cult': 2}


# Make a list of options of factions to play weighted away from factions played previously.
def options_from_history(history=None):
    options = []
    options.extend(all_factions)
    if history is not None:
        if isinstance(history, str):
            history = [history]
        for h in history:
            options.extend(all_factions)
            options.remove(h)
    return options


class Faction:
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = random.choice(all_factions)
        self.reach = reach[self.name]

    def __repr__(self):
        return self.name


class Player:
    def __init__(self, name, faction=None, history=None):
        self.name = name
        self.history = history
        self.options = options_from_history(self.history)
        if faction:
            self.faction = faction
        else:
            self.faction = random.choice(self.options)

    def __repr__(self):
        return self.name


def calculate_reach(factions):
    for i, f in enumerate(factions):
        if isinstance(f, str):
            factions[i] = Faction(f)
    total_reach = sum([faction.reach for faction in factions])
    names = [faction.name for faction in factions]
    count_vagabonds = names.count('Vagabond')
    if count_vagabonds > 1:
        total_reach -= 2
    return total_reach


def select_faction(player=None):
    if isinstance(player, Player):
        return random.choice(player.options)
    else:
        return random.choice(all_factions)


def randomize(players=4):
    if isinstance(players, int):
        players = range(players)

    def test_duplicates(selected):
        # TODO: allow for double vagabonds
        return len(selected) != len(set(selected))

    def test_low_reach(selected):
        reach_min = {2: 17, 3: 18, 4: 21, 5: 25, 6: 28}
        return calculate_reach(selected) < reach_min[len(selected)]

    # TODO: add feature to add weight to a faction (add Lizard Cult x times to end of options list)

    s = [select_faction(player) for player in players]
    while test_duplicates(s) | test_low_reach(s):
        s = [select_faction(player) for player in players]
    return s


def read_history(column):
    return pd.read_excel(r'C:\Users\brlw\Desktop\Root.xlsx',
                         usecols=column, skiprows=2, header=None
                         ).dropna().iloc[:, 0].values


