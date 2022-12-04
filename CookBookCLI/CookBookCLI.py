from .models import Ingredient, Recipie
from .ui_components import test


i = Ingredient("Sugar", 5, "tsp")
r = Recipie("Crepes")

r.ingredients.append(i)
r.directions = ["First you want to crack the egg", "Then you wanna put it in da bowl :O", "And then cook it ;);)"]
r.edit()

print(i, r)

