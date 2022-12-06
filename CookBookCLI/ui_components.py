import json
import time
import os
import shutil

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
            choices = ['Search', 'View all recipies', 'Compile to markdown', 'Write new recipie', 'Exit']
            title = 'What would you like to do?'
              
            selected = menu.show(title, choices, position = last_selected)
            last_selected = selected 
            choice = choices[selected]
            print()

            if choice == "Exit":
                with open(self.path, "w") as file:
                    json.dump(self.recipies, file)
                return
            
            elif choice == "Search":
                self.search()

            elif choice == "View all recipies":
                self.view_all()

            elif choice == "Compile to markdown":
                self.compile()

            elif choice == "Write new recipie":
                self.write_new()

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
        shutil.rmtree("recipies/")
        os.mkdir("recipies/")
        
        for i in utils.categories:
            os.mkdir(f"recipies/{i}")
        
        for name, data in self.recipies.items():
            os.mkdir(f"recipies/{data['meta']['category']}/{name}")

            with open(f"recipies/{data['meta']['category']}/{name}/README.md", "w") as file:
                r = Recipie(name).load_from_json(data)
                out = r.get_str()
                out = "\n".join(out.split("\n")[2:])
                file.write(out)

    def write_new(self):
        logger.print(logger.print_string_constructor(
            'What should we call the recipie?', 
            '[?] ',
            cli_utility.colorama.Fore.LIGHTBLUE_EX,
        ))
        name = utils.input("> ", "")
        if name in self.recipies:
            logger.print_error("That recipie already exsists.")
            utils.wait()
            return

        r = Recipie(name)
        r.edit()
        self.recipies[name] = r.dump_to_json()


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
