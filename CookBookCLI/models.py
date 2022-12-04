import time

from .cli_utility import cli_utility
from .utils import Utils

menu = cli_utility.cli_menu(False)
logger = cli_utility.output_manager()
utils = Utils()

class Ingredient:
    """ Ingredient object """
    def __init__(self, name: str, amount: float, unit: str) -> None:
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

        self.ingredients = []
        self.directions = []

    def __repr__(self):
        return f"<Recipie {self.title}>"

    def get_str(self):
        out = f"Editing: /{self.category}/{self.title}\n\n"
        out += f"# {self.title}\n\n"
        out += "Author | Total Cook Time | Portions  \n"
        out += "-------|-----------------|---------  \n"
        out += f"{self.author} | {self.cook_time} | {self.portions}  \n\n"
        out += "## Ingredients  \n"
        for i in self.ingredients:
            out += f" - {i.get_name()}  \n"
        out += "\n## Method  \n"
        for i, item in zip(range(len(self.directions)), self.directions):
            out += f"{i+1}. {item}  \n"

        return out

    def edit(self):
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
              
            selected = menu.show(title, choices)
            choice = choices[selected]
            print()

            if choice == "Metadata":
                self.edit_meta()
            elif choice == "Ingredients":
                self.edit_ingredient()
            elif choice == "Materials":
                self.edit_materials()
            elif choice == "Method":
                self.edit_method()
            elif choice == "Exit":
                return
            #logger.print('Now editing:',
            #             fore_color=cli_utility.colorama.Fore.LIGHTCYAN_EX)
            #logger.print_success(choice)

    def edit_meta(self):
        """
        A loop to edit the metadata of the recipie, information such as author and cook time
        """

        while True:
            utils.clear()
            print(self.get_str())

            choices = ["Author", "Categorry", "Cook time", "Portions", "Exit"]
            title = 'What would you like to edit?'
              
            selected = menu.show(title, choices)
            choice = choices[selected]
            print()

            if choice == "Author":
                logger.print(logger.print_string_constructor(
                    'Author, a discord username / tag is recommended for consistency', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))
                self.author = utils.input("> ", self.author)

            elif choice == "Categorry":
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
        while True:
            utils.clear()
            print(self.get_str())

            choices = [i.get_name() for i in self.ingredients] + ["New ingredient", "Exit"]
            title = 'Choose an ingredient'
              
            selected = menu.show(title, choices)
            choice = selected
            print()

            # If the user selects "new ingredient"
            if choice == len(self.ingredients):
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

            ingredient = self.ingredients[choice]
            print(choice, len(self.ingredients))

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

            elif choice == "Exit":
                return

    def edit_method(self):
        """
        Edit the method section
        """
        while True:
            utils.clear()
            print(self.get_str())

            choices = [i for i in self.directions] + ["Create new", "Create new after exsisting", "Exit"]
            title = 'Choose a direction'
              
            selected = menu.show(title, choices)
            choice = selected
            print(choice, selected, len(self.directions))
            print()

            # If the user selects "new direction"
            if choice == len(self.directions):
                logger.print(logger.print_string_constructor(
                    'Create a new direction', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))

                direction = input("> ")
                self.directions.append(direction)

            # If user selectes "Create after"
            elif choice == len(self.directions)+1:
                choices = [i for i in self.directions] + ["Exit"]
                title = 'Where do you want the new direction (after selected element)'
                  
                selected = menu.show(title, choices)
                choice = selected
                logger.print(logger.print_string_constructor(
                    'Create a new direction', 
                    '[?] ',
                    cli_utility.colorama.Fore.LIGHTBLUE_EX,
                ))

                direction = input("> ")
                self.directions.insert(choice+1, direction)

            # If user selectes "Exit"
            elif choice == len(self.directions)+2:
                return


            logger.print(logger.print_string_constructor(
                'Edit the direction.', 
                '[?] ',
                cli_utility.colorama.Fore.LIGHTBLUE_EX,
            ))
            self.directions[choice] = utils.input("> ", self.directions[choice])
            


    def add_ingredient(self, name: str, amount: float, unit: str) -> None:
        """
        Add an ingredient in the recipie

        Parameters:
        name - Name of the ingredient, eg. "sugar"
        amount - The amount of that ingredient
        unit - What unit of messurement we are using
        """
        self.ingredients.append(Ingredient(name, amount, unit)) 
