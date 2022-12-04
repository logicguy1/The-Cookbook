from .cli_utility import cli_utility

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
