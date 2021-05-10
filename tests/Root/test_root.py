from BoardGames.Root import Randomizer


def test_all_factions():
    assert len(Randomizer.all_factions) == 6


def test_reach():
    assert Randomizer.reach['Vagabond'] == 5


def test_options_history():
    assert Randomizer.options_from_history() == Randomizer.all_factions
    assert (Randomizer.options_from_history('Marquise de Cat') ==
            ['Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond',
             'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult'])
    assert (Randomizer.options_from_history(['Marquise de Cat']) ==
            ['Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond',
             'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult'])
    assert (Randomizer.options_from_history(['Marquise de Cat', 'Marquise de Cat']) ==
            ['Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult'])


def test_faction():
    faction = Randomizer.Faction(name='Woodland Alliance')
    assert faction.name == 'Woodland Alliance'
    assert faction.reach == 3
    assert Randomizer.Faction().name in Randomizer.all_factions


def test_player():
    player = Randomizer.Player('player1')
    assert player.name == 'player1'
    assert player.history is None
    assert player.faction in Randomizer.all_factions
    player = Randomizer.Player('player2',
                               faction='Lizard Cult',
                               history=['Vagabond', 'Lizard Cult', 'Woodland Alliance'])
    assert player.faction == 'Lizard Cult'
    assert (player.options ==
            ['Marquise de Cat', 'Eyrie Dynasties', 'Riverfolk Company',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
             'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult'])


def test_calculate_reach():
    assert Randomizer.calculate_reach(['Marquise de Cat', 'Eyrie Dynasties', 'Riverfolk Company', 'Vagabond']) == 27
    assert Randomizer.calculate_reach(['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Vagabond']) == 25


def test_select_faction():
    p1 = Randomizer.Player('player1')
    p2 = Randomizer.Player('player2')
    assert Randomizer.select_faction(p1) in Randomizer.all_factions
    assert Randomizer.select_faction() in Randomizer.all_factions
