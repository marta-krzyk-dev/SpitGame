from Project4_Split.ConsolePrinter import ConsolePrinter
from Project4_Split.helpers import getFirst


class CardPrinter(ConsolePrinter):
    def __init__(self, font_color="white"):
        ConsolePrinter.__init__(self, font_color)

    def PrintCardPiles(self, card_piles, print_size_above_cards=False, print_size_below_cards=False):
        row1 = ""
        row2 = ""
        row3 = ""
        pile_sizes_row = ""

        for pile in card_piles:
            row1 += "┌──┐  " if len(pile) < 2 else "╔══╗  "
            character = getFirst(pile, '░')
            row2 += f"│{character.ljust(2)}│  " if len(pile) < 2 else f"║{character.ljust(2)}║  "
            row3 += "└──┘  " if len(pile) < 2 else "╚══╝  "
            pile_sizes_row += f"[{str(len(pile))}]".rjust(4) + "  " if len(pile) > 1 else " " * 6

        if print_size_above_cards:
            self.PrintCentered(pile_sizes_row)

        self.PrintCentered(row1)
        self.PrintCentered(row2)
        self.PrintCentered(row3)

        if print_size_below_cards:
            self.PrintCentered(pile_sizes_row)
