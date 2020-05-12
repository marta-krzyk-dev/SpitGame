from Project4_Split.helpers import getFirst
from termcolor import colored


def PrintCardPiles(card_piles, font_color, print_size_above_cards=False, print_size_below_cards=False):
    row1 = ""
    row2 = ""
    row3 = ""
    pile_sizes_row = ""

    for pile in card_piles:
        row1 += "┌──┐  " if len(pile) < 2 else "╔══╗  "
        character = getFirst(pile, '░')
        row2 += f"│{character.ljust(2)}│  " if len(pile) < 2 else f"║{character.ljust(2)}║  "
        row3 += "└──┘  " if len(pile) < 2 else "╚══╝  "
        pile_sizes_row += f"[{str(len(pile))}]".rjust(4) + "  "

    if print_size_above_cards:
        print(colored(pile_sizes_row.center(50), font_color, attrs=["bold"]))

    print(colored(row1.center(50), font_color, attrs=["bold"]))
    print(colored(row2.center(50), font_color, attrs=["bold"]))
    print(colored(row3.center(50), font_color, attrs=["bold"]))

    if print_size_below_cards:
        print(colored(pile_sizes_row.center(50), font_color, attrs=["bold"]))
