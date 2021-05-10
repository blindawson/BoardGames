import random

all_factions = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond',
                'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult']


def options_from_history(history):
    options = []
    options.extend(all_factions)
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
        reach = {'Marquise de Cat': 10,
                 'Eyrie Dynasties': 7,
                 'Vagabond': 5,
                 'Riverfolk Company': 5,
                 'Woodland Alliance': 3,
                 'Lizard Cult': 2}
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
    reach = sum([faction.reach for faction in factions])
    names = [faction.name for faction in factions]
    count_vagabonds = names.count('vagabond')
    if count_vagabonds > 1:
        reach -= 2
    return reach


def select_faction(player=None):
    if isinstance(player, Player):
        return random.choice(player.options)
    else:
        return random.choice(all_factions)


def randomize(players=4):

    def select_factions():
        if isinstance(players, int):
            num_players = players
        else:
            num_players = len(players)
        return [random.choice(all_factions) for i in range(num_players)]

    def test_duplicates(selected):
        return len(selected) != len(set(selected))

    def test_low_reach(selected):
        reach_min = {2: 17, 3: 18, 4: 21, 5: 25, 6: 28}
        return calculate_reach(selected) < reach_min[len(selected)]

    s = select_factions()
    while test_duplicates(s) | test_low_reach(s):
        s = select_factions()
    return s


bml = Player(name='Lindawson', history=['Marquise de Cat', 'Marquise de Cat'])