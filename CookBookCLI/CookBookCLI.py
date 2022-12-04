from .models import Ingredient, Recipie
from .ui_components import test


i = Ingredient("Sugar", 5, "tsp")
r = Recipie("Crepes")

r.ingredients.append(i)
r.edit()

print(i, r)

