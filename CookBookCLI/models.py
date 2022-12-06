import time

from .cli_utility import cli_utility
from .utils import Utils

menu = cli_utility.cli_menu(False)
logger = cli_utility.output_manager()
utils = Utils()

class Ingredient:
    """ Ingredient object """
    def __init__(self, name: str, amount: str, unit: str) -> None:
        self.name = name
        self.amount = amount
        self.unit = unit

    def __repr__(self):
        return f"<Ingredient {self.name}>"

    def get_name(self):
        """
        Return the ingredient as a string
        """
        return f"{self.name}, {self.amount} {self.unit}"


class Recipie:
    """ Recipie object """
    def __init__(self, title):
        self.title = title

        # Metadata
        self.category = utils.categories[0]
        self.author = ""
        self.cook_time = ""
        self.portions = ""

        # Ordered and unordered lists
        self.ingredients = []
        self.directions = []
        self.materials = []

        # Textareas
        self.conclusion = ""
        self.discussion = ""

    def __repr__(self):
        return f"<Recipie {self.title}>"

    def load_from_json(self, data: dict) -> None:
        # Metadata
        self.category = data["meta"]["category"]
        self.author = data["meta"]["author"]
        self.cook_time = data["meta"]["cook_time"]
        self.portions = data["meta"]["portions"]

        # Ordered and unordered lists
        self.ingredients = list(map(
                lambda i: Ingredient(i["name"], i["amount"], i["unit"]), 
                data["ingredients"]))
        self.materials = data["materials"]
        self.directions = data["method"]

        # Textareas
        self.conclusion = data["conclusion"]
        self.discussion = data["discussion"]

        return self

    def dump_to_json(self) -> dict:
        out = {
                "meta": {
                    "author": self.author,
                    "category": self.category,
                    "cook_time": self.cook_time,
                    "portions": self.portions,
                },
                "ingredients": [{"name": i.name, "amount": i.amount, "unit": i.unit} for i in self.ingredients],
                "materials": self.materials,
                "method": self.directions,
                "conclusion": self.conclusion,
                "discussion": self.discussion
        }
        return out

    def get_str(self):
        out = f"Editing: /{self.category}/{self.title}\n\n"
        out += f"# {self.title}\n\n"

        len_auth = utils.clamp_up(6, len(self.author))
        len_cook = utils.clamp_up(15, len(self.cook_time))
        len_port = utils.clamp_up(8, len(self.portions))

        out += f"{'Author':<{len_auth}} | {'Total Cook Time':<{len_cook}} | {'Portions':<{len_port}}  \n"
        out += f"{'-'*len_auth}-|-{'-'*len_cook}-|-{'-'*len_port}  \n"
        out += f"{self.author:<{len_auth}} | {self.cook_time:<{len_cook}} | {self.portions:<{len_port}}  \n\n"

        out += "## Ingredients  \n"
        for i in self.ingredients:
            out += f" - {i.get_name()}  \n"

        out += "\n## Materials  \n"
        for i in self.materials:
            out += f" - {i}  \n"

        out += "\n## Method  \n"
        for i, item in zip(range(len(self.directions)), self.directions):
            out += f"{i+1}. {item}  \n"

        out += "\n## Conclusion  \n"
        out += self.conclusion + "  \n"
        out += "\n## Discussion  \n"
        out += self.discussion + "  \n"

        return out

    def edit(self):
        last_selected = 0
        while True:
            utils.clear()
            print(self.get_str())

            choices = [
                    'Metadata', 
                    'Ingredients', 
                    'Materials', 
                    'Method', 
                    'Conclusion', 
                    'Discussion', 
                    'Exit'
            ]
            title = 'What would you like to edit?'
              
            selected = menu.show(title, choices, position = last_selected)
            last_selected = selected 
            choice = choices[selected]
            print()

            if choice == "Metadata":
                self.edit_meta()
            elif choice == "Ingredients":
                self.edit_ingredient()
            elif choice == "Materials":
                self.materials = self.edit_list(self.materials)
            elif choice == "Method":
                self.directions = self.edit_list(self.directions)
            elif choice == "Conclusion":
                logger.print(logger.print_string_constructor(
                    'This is where you can conclude your recipie, what is the recipient left with at the end, is there a specific way to eat it? Be creative!', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.conclusion = utils.input("> ", self.conclusion)

            elif choice == "Discussion":
                logger.print(logger.print_string_constructor(
                    'In this segment you can talk about ways to change up the recipie for the indevidual person, if you have tried something you thought could work but have not comitted to it yet as a part of the recipie.', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.discussion = utils.input("> ", self.discussion)

            elif choice == "Exit":
                return
            #logger.print('Now editing:',
            #             fore_color=cli_utility.colorama.Fore.LIGHTCYAN_EX)
            #logger.print_success(choice)

    def edit_meta(self):
        """
        A loop to edit the metadata of the recipie, information such as author and cook time
        """
        last_selected = 0
        while True:
            utils.clear()
            print(self.get_str())

            choices = ["Author", "Category", "Cook time", "Portions", "Exit"]
            title = 'What would you like to edit?'
              
            selected = menu.show(title, choices, position=last_selected)
            last_selected = selected
            choice = choices[selected]
            print()

            if choice == "Author":
                logger.print(logger.print_string_constructor(
                    'Author, a discord username / tag is recommended for consistency', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.author = utils.input("> ", self.author)

            elif choice == "Category":
                choices = utils.categories 
                title = 'What category discribes your dish best?'
                  
                selected = menu.show(title, choices)
                choice = choices[selected]
                self.category = choice

            elif choice == "Cook time":
                logger.print(logger.print_string_constructor(
                    'How much time should the user expect to spend on the dish. Eg. "prep: 30 minutes, cook: 25 minutes".', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.cook_time = utils.input("> ", self.cook_time)

            elif choice == "Portions":
                logger.print(logger.print_string_constructor(
                    'How many does it feed / how many dishes does it produce? Eg. 12 pancakes.', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.portions = utils.input("> ", self.portions)
            elif choice == "Exit":
                return

    def edit_ingredient(self):
        """
        A loop to edit add or remove ingredients from the list
        """
        last_selected = 0
        while True:
            utils.clear()
            print(self.get_str())

            choices = [i.get_name() for i in self.ingredients] + ["New ingredient", "Exit"]
            title = 'Choose an ingredient'
              
            selected = menu.show(title, choices, position=last_selected)
            choice = selected
            print()

            # If the user selects "new ingredient"
            if choice == len(self.ingredients):
                last_selected += 1
                logger.print(logger.print_string_constructor(
                    'Ingredient, format: "<name>, <amount> <unit>"', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))

                while True:
                    ingredient = input("> ")
                    try:
                        name, amount = ingredient.split(", ")
                        amount, unit = amount.split(" ")
                        break
                    except ValueError:
                        logger.print_error("Invalid ingredient, please follow format.")

                self.ingredients.append(Ingredient(name, amount, unit))
                continue

            # If user selectes "Exit"
            elif choice == len(self.ingredients)+1:
                return

            # If the user selectes anything else
            ingredient = self.ingredients[choice]

            choices = ['Edit', 'Delete', 'Exit']
            title = 'What would you like to do?'
              
            selected = menu.show(title, choices)
            choice = choices[selected]
            print()

            if choice == "Edit":
                logger.print(logger.print_string_constructor(
                    'Edit a ingredient, format: "<name>, <amount> <unit>"', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                while True:
                    i = utils.input("> ", ingredient.get_name())
                    try:
                        name, amount = i.split(", ")
                        amount, unit = amount.split(" ")
                        break
                    except ValueError:
                        logger.print_error("Invalid ingredient, please follow format.")
                
                self.ingredients[self.ingredients.index(ingredient)] = Ingredient(name, amount, unit) 
                print()

            elif choice == "Delete":
                del self.ingredients[self.ingredients.index(ingredient)]
                last_selected -= 1

            elif choice == "Exit":
                return

    def edit_list(self, arr: list) -> list:
        """
        Edit a list of strings section
        
        Parameters:
        arr - A python list object pobulated with strings
        """
        last_selected = 0
        while True:
            utils.clear()
            print(self.get_str())

            size = utils.get_size()
            choices = [i[:size[0] - 6].replace("\n", "\\n") for i in arr] + ["Create new", "Create new after existing", "Exit"]
            title = 'Choose an element or action. '
              
            selected = menu.show(title, choices, position=last_selected)
            last_selected = selected
            choice = selected
            print()

            # If the user selects "new direction"
            if choice == len(arr):
                last_selected += 1
                logger.print(logger.print_string_constructor(
                    'Create a new element', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))

                direction = input("> ")
                arr.append(direction)

            # If user selectes "Create after"
            elif choice == len(arr)+1:
                size = utils.get_size()
                choices = [i[:size[0] - 6].replace("\n", "\\n") for i in arr] + ["Exit"]
                title = 'Where do you want the element (after selected element)'
                  
                selected = menu.show(title, choices)
                choice = selected
                if choice != len(arr):
                    logger.print(logger.print_string_constructor(
                        'Create a new element', 
                        '[?] ',
                        cli_utility.colorama.Fore.LIGHTBLUE_EX,
                    ))

                    direction = input("> ")
                    arr.insert(choice+1, direction)

            # If user selectes "Exit"
            elif choice == len(arr)+2:
                return arr


            else:
                logger.print(logger.print_string_constructor(
                    'Edit the element or leave empty to remove.', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                inp = utils.input("> ", arr[choice])
                if inp != "":
                    arr[choice] = inp
                else:
                    del arr[choice]

        return arr

            
