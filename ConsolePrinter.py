from termcolor import colored, COLORS
from os import system, get_terminal_size


class ConsolePrinter:
    # region Constructor
    def __init__(self, font_color="white"):
        self.font_color = font_color if font_color in COLORS.keys() else "white"
        try:
            self.console_width = get_terminal_size().columns
        except OSError:
            self.console_width = 50
    # endregion

    # region Methods
    def ClearConsole(self):
        system('cls')

    def Print(self, text, color=None, attributes=["bold"]):
        if not isinstance(text, str):
            return
        else:
            if color is None:
                color = self.font_color
            print(colored(text, color, attrs=attributes))

    def PrintCentered(self, text, font_color=None, attributes=["bold"]):
        if font_color is None:
            font_color = self.font_color

        print(colored(text.center(self.console_width), font_color, attrs=attributes))

    def PrintReverse(self, text):
        self.Print(text, self.font_color, ["bold", "reverse"])

    def PrintOnBackground(self, text):
        if not isinstance(text, str):
            return

        print(colored(text, self.font_color, attrs=["bold", "reverse"]))

    def PrintParagraphs(self, paragraphDict):
        if not isinstance(paragraphDict, dict):
            return

        for p in paragraphDict:
            self.Print(f"\n*** {p.upper()} ***\n", "blue", ['bold', 'reverse'])
            print(colored(paragraphDict[p], "white", attrs=['bold']))

        if len(paragraphDict) > 0:
            print()
    # endregion