import numpy as np
from BoardGames.Root import Randomizer

lindawson_h, fiendfellow_h, rootaphile_h, bdlocas_h = Randomizer.read_history()

lindawson = Randomizer.Player('Lindawson', history=lindawson_h)
fiendfellow = Randomizer.Player('FiendFellow', history=fiendfellow_h)
rootaphile = Randomizer.Player('Rootaphile', history=rootaphile_h)
bdlocas = Randomizer.Player('bdlocas', history=bdlocas_h)
players = [lindawson, fiendfellow, rootaphile, bdlocas]

n = 10000
analysis = [Randomizer.randomize(players) for i in range(n)]


def faction_chance(results, faction):
    return round(sum(faction in r for r in results)/len(results)*100)


def double_vagabond_chance(results):
    return round(sum((r.count('Vagabond') == 2) for r in results)/len(results)*100)


print('Chance of each faction being in the game:')
for f in Randomizer.all_factions:
    print(f'{f}: {faction_chance(analysis, f)}%')
print(f'Double Vagabonds: {double_vagabond_chance(analysis)}%')


def print_player_odds(results, player):
    player_order = {'Lindawson': 0, 'FiendFellow': 1, 'Rootaphile': 2, 'bdlocas': 3}
    player_row = np.array(results)[:, player_order[player.name]]
    print(f'\n{player} Actual Odds:')
    for fa in Randomizer.all_factions:
        print(f'{fa}: {round(np.sum(player_row == fa)/len(player_row)*100)}%')


def print_player_odds_original(player):
    print(f'\n{player} Original Odds:')
    for fa in Randomizer.all_factions:
        print(f'{fa}: {round(player.options.count(fa)/len(player.options)*100)}%')


for p in players:
    print_player_odds_original(p)
    print_player_odds(analysis, p)

print(Randomizer.randomize(players))
