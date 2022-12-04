import json

from .models import Ingredient, Recipie
from .ui_components import test


r = Recipie("The Chef's cookies")

#with open("CookBookCLI/recipies.json", "r") as file:
#    data = json.load(file)
#    print(data)
#    # r.load_from_json(data["Crepes"])

data = {"Crepes": {'meta': {'author': 'Nouille#2370', 'category': 'Desserts', 'cook_time': 'About 15 miuntes', 'portions': 'Can feed 2-3 people'}, 'ingredients': [{'name': 'Flour T65', 'amount': '200', 'unit': 'grams'}, {'name': 'Cornstarch', 'amount': '50', 'unit': 'grams'}, {'name': 'eggs', 'amount': '2', 'unit': 'peaces'}, {'name': 'Milk', 'amount': '50', 'unit': 'cl'}, {'name': 'Salt', 'amount': '1', 'unit': 'pinch'}, {'name': 'Melted butter', 'amount': '50', 'unit': 'grams'}], 'materials': ['A big bowl', 'A wisk', 'A pan', 'A ladle'], 'method': ["Add every ingredients in the bowl and mix.  \\n*Tip*: Put all the liquids first and then pour the flour and the cornstarch in. It'll prevent lumps.", 'Heat the pan', 'Pour a ladle of the mix in the pan and spread the liquid by moving the pan around.', 'Flip the crêpe around when the side on the pan appears brown.', 'Wait a minute and put your crêpe on a plate. Done!'], 'conclusion': "Crêpes is one of the easiest recipe I've ever tried. And it is good.", 'discussion': 'I recommend putting some sugar on top of your crêpe and then fold it, it is my personal favorite. But you can pretty much put anything on your crêpes, even salty things like cheese or ham! Be creative!'}}

r.edit()

with open("CookBookCLI/recipies.json", "w") as file:
    data[r.title] = r.dump_to_json()
    json.dump(data, file, indent=2)

