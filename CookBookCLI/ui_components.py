import json
import time

from .cli_utility import cli_utility
from .utils import Utils
from .models import Recipie

menu = cli_utility.cli_menu(False)
logger = cli_utility.output_manager()
utils = Utils()


class Client:
    def __init__(self, path: str = "") -> None:
        if path == "":
            logger.print(logger.print_string_constructor(
                'Input a relative or abselute path to json recipie file.', 
                '[?] ',
                cli_utility.colorama.Fore.LIGHTBLUE_EX,
            ))
            path = utils.input("> ", "CookBookCLI/recipies.json")

        self.path = path
        with open(path, "r") as file:
            self.recipies = json.load(file)

    def show(self) -> None:
        last_selected = 0
        while True:
            utils.clear()
            choices = ['Search', 'View all recipies', 'Compile to markdown', 'Exit']
            title = 'What would you like to do?'
              
            selected = menu.show(title, choices, position = last_selected)
            last_selected = selected 
            choice = choices[selected]
            print()

            if choice == "Exit":
                return
            
            elif choice == "Search":
                self.search()

            elif choice == "View all recipies":
                self.view_all()

            elif choice == "Compile to markdown":
                self.compile()

            else:
                pass

    def show_recipies(self, recipies: list) -> None:
        last_selected = 0
        while True:
            choices = recipies
            title = 'What recipie should we open?'
              
            selected = menu.show(title, choices, position = last_selected)
            last_selected = selected 
            choice = choices[selected]
            print()

            if choice == "Exit":
                break

            else:
                choices = ['View', 'Edit']
                title = 'What would you like do?'
                  
                selected = menu.show(title, choices)

                if selected == 0:
                    r = Recipie(choice)
                    r.load_from_json(self.recipies[choice])
                    print(r.get_str())
                    utils.wait()

                elif selected == 1:
                    r = Recipie(choice)
                    r.load_from_json(self.recipies[choice])
                    r.edit()
                    data = r.dump_to_json()
                    self.recipies[choice] = data

    def view_all(self) -> None:
        last_selected = 0
        while True:
            utils.clear()
            choices = utils.categories + ['Exit']
            title = 'What category should we open?'
              
            selected = menu.show(title, choices, position = last_selected)
            last_selected = selected 
            category = choices[selected]

            if category == "Exit":
                return

            self.show_recipies(sorted([k for k, v in self.recipies.items() \
                           if v["meta"]["category"] == category]) \
                           + ['Create new', 'Exit'])

    def search(self) -> None:
        logger.print(logger.print_string_constructor(
            'Input a search query.', 
            '[?] ',
            cli_utility.colorama.Fore.LIGHTBLUE_EX,
        ))
        query = utils.input("> ", "")
        found = [k for k, v in self.recipies.items() if query.lower() in json.dumps(v).lower()]
        print()

        if len(found) == 0:
            logger.print_error("No results found")
            utils.wait()

        self.show_recipies(found + ["Exit"])

    def compile(self) -> None:
        pass
        




def test():
    menu = cli_utility.cli_menu(False)
    logger = cli_utility.output_manager()
      
    choices = ['Ingredients', 'Materials', 'Method', 'Conclusion', 'Discussion']
    title = 'What would you like to edit?'
      
    selected = menu.show(title, choices)
    choice = choices[selected]
    logger.print('Now editing:',
                 fore_color=cli_utility.colorama.Fore.LIGHTCYAN_EX)
    logger.print_success(choice)
