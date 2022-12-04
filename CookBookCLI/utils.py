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

    def clamp_up(self, num1: int, num2: int) -> int:
        return max((num1, num2))

    def get_size(self) -> tuple:
        size = os.get_terminal_size()
        return size.columns, size.lines
