from BoardGames.Root import Randomizer

lindawson_history = Randomizer.read_history('C')
fiendfellow_history = Randomizer.read_history('F')
rootaphile_history = Randomizer.read_history('I')
bdlocas_history = Randomizer.read_history('L')

lindawson = Randomizer.Player('Lindawson', history=lindawson_history)
fiendfellow = Randomizer.Player('FiendFellow', history=fiendfellow_history)
rootaphile = Randomizer.Player('Rootaphile', history=rootaphile_history)
bdlocas = Randomizer.Player('bdlocas', history=bdlocas_history)

print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
# print(Randomizer.randomize([lindawson, fiendfellow, rootaphile, bdlocas]))
