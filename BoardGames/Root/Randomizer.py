import random
import itertools
from googleapiclient.discovery import build
from google.oauth2 import service_account

all_factions = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond',
                'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult']
reach = {'Marquise de Cat': 10,
         'Eyrie Dynasties': 7,
         'Vagabond': 5,
         'Riverfolk Company': 5,
         'Woodland Alliance': 3,
         'Lizard Cult': 2}
reach_min = {2: 17, 3: 18, 4: 21, 5: 25, 6: 28}


# Make a list of options of factions to play weighted away from factions played previously.
def options_from_history(history=None):
    options = []
    if history is not None:
        if isinstance(history, str):
            history = [history]
        for h in history:
            try:
                options.remove(h)
            except ValueError:
                options.extend(all_factions)
                options.remove(h)
    options.extend(all_factions)
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
    def __init__(self, name, history=None):
        self.name = name
        self.history = history
        self.options = options_from_history(self.history)

    def __repr__(self):
        return self.name


def calculate_reach(factions):
    total_reach = sum([Faction(faction).reach for faction in factions])
    count_vagabonds = factions.count('Vagabond')
    if count_vagabonds == 2:
        total_reach -= 3
    return total_reach


def select_faction(player=None):
    if isinstance(player, Player):
        return random.choice(player.options)
    else:
        return random.choice(all_factions)


def test_duplicates(selected, allow2vagabonds=True):
    if allow2vagabonds & (selected.count('Vagabond') == 2):
        return len(selected) != len(set(selected)) + 1
    else:
        return len(selected) != len(set(selected))


def randomize(players=4):
    if isinstance(players, int):
        players = range(players)

    def test_low_reach(selected):
        return calculate_reach(selected) < reach_min[len(selected)]

    # TODO: TEST FOR LOW REACH
    # TODO: add optional feature to add custom weights for choosing factions
    # TODO: add optional feature so you don't play the same faction twice in a row

    s = [select_faction(player) for player in players]
    while test_duplicates(s) | test_low_reach(s):
    # while test_duplicates(s):
        s = [select_faction(player) for player in players]
    return s


def read_history():
    SERVICE_ACCOUNT_FILE = r'C:\Users\brlw\Desktop\Repositories\BoardGames\BoardGames\Root\keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    spreadsheet = '1Fe_M9Xtweh_GjggHKSe0FaoruKiGBXj1hkQEHyH38u4'
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet, range=f'Sheet1!C:L').execute()
    values = list(itertools.chain.from_iterable(result.get('values', [])[2:]))
    p1 = values[::10]
    p2 = values[3::10]
    p3 = values[6::10]
    p4 = values[9::10]
    return p1, p2, p3, p4
