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
    player = Randomizer.Player('player2',
                               history=['Vagabond', 'Lizard Cult', 'Woodland Alliance'])
    # TODO: update the test for player options
    # assert (player.options ==
    #         ['Marquise de Cat', 'Eyrie Dynasties', 'Riverfolk Company',
    #          'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
    #          'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult',
    #          'Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company', 'Woodland Alliance', 'Lizard Cult'])


def test_calculate_reach():
    assert Randomizer.calculate_reach(['Marquise de Cat', 'Eyrie Dynasties', 'Riverfolk Company', 'Vagabond']) == 27
    assert Randomizer.calculate_reach(['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Vagabond']) == 24
    # TODO: Test a bunch of times for many player counts and confirm it always comes above the reach min


def test_select_faction():
    p1 = Randomizer.Player('player1')
    assert Randomizer.select_faction(p1) in Randomizer.all_factions
    assert Randomizer.select_faction() in Randomizer.all_factions


def test_test_duplicates():
    s = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Riverfolk Company']
    assert ~Randomizer.test_duplicates(s)
    s = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Eyrie Dynasties']
    assert Randomizer.test_duplicates(s)
    s = ['Marquise de Cat', 'Eyrie Dynasties', 'Vagabond', 'Vagabond']
    assert ~Randomizer.test_duplicates(s, allow2vagabonds=True)
    assert Randomizer.test_duplicates(s, allow2vagabonds=False)


def test_randomize():
    assert isinstance(Randomizer.randomize()[3], str)
