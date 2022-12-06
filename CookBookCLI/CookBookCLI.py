import json

from .models import Ingredient, Recipie
from .ui_components import test, Client

client = Client()
client.show()


"""
with open("CookBookCLI/recipies.json", "r") as file:
    data = json.load(file)
    print(data)
    r.load_from_json(data["Crepes"])


r.edit()

with open("CookBookCLI/recipies.json", "w") as file:
    data[r.title] = r.dump_to_json()
    json.dump(data, file, indent=2)
"""
