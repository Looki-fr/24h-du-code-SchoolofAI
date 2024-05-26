from InquirerPy import inquirer
from colorama import Fore, Style, init

class InquireHelper:
    def __init__(self):
        # Initialize colorama for colored output
        init(autoreset=True)
        self.colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "blue": Fore.BLUE,
            "yellow": Fore.YELLOW,
            "cyan": Fore.CYAN,
            "magenta": Fore.MAGENTA,
            "white": Fore.WHITE
        }

    def print(self, text, color):
        color_code = self.colors.get(color.lower(), Fore.WHITE)
        print(f"{color_code}{text}")
    
    def input(self,text, color):
        color_code = self.colors.get(color.lower(), Fore.WHITE)
        return input(f"{color_code}{text}")

# Example usage of InquireHelper
if __name__ == "__main__":
    helper = InquireHelper()
    helper.print("This is a red text", "red")
    helper.print("This is a green text", "green")
    helper.prompt_user()
