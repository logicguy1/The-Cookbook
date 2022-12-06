import readline
import os

class Utils:
    categories = [
        "Bread",
        "Starters",
        "Main courses",
        "Drinks",
        "Desserts",
        "Snacks"
    ]

    def input(self, prompt: str, text: str) -> str:
        """
        Show an input field with predefined text
        WARNING: May not work on windows machines / python emulators, has not been properly tested
        """
        try:
            def hook():
                readline.insert_text(text)
                readline.redisplay()
            readline.set_pre_input_hook(hook)
            result = input(prompt)
            readline.set_pre_input_hook()
            return result
        except KeyboardInterrupt:
            readline.set_pre_input_hook()
            raise KeyboardInterrupt

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""  ___            _    ___            _     ___  _     ___
 / __| ___  ___ | |__| _ ) ___  ___ | |__ / __|| |   |_ _|
| (__ / _ \/ _ \| / /| _ \/ _ \/ _ \| / /| (__ | |__  | |
 \___|\___/\___/|_\_\|___/\___/\___/|_\_\ \___||____||___|

 By Drillenissen       Version 0.1          Time 14:08:34
              """)

    def clamp_up(self, num1: int, num2: int) -> int:
        return max((num1, num2))

    def get_size(self) -> tuple:
        size = os.get_terminal_size()
        return size.columns, size.lines

    def wait(self) -> None:
        if os.name == "nt":
            os.system("pause")
        else:
            os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
            print()
