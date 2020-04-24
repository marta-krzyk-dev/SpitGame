import termcolor
from termcolor import colored
from Project4_Split.helpers import getFirst, tryConvertToInt
from Project4_Split.ConsoleInputOutputManipulator import ConsoleInputOutputManipulator

class Player(ConsoleInputOutputManipulator):
    def __init__(self, name, cards, pile_count, pile_names, color="green"):

        ConsoleInputOutputManipulator.__init__(self, color)
        self.card_piles = []

        self.spit_pile = []
        self.pile_count = pile_count
        self.name = name
        self.pile_names = pile_names
        self.color = color if color in termcolor.COLORS.keys() else "green"

        self.ReceiveCards(cards)

    def ReceiveCards(self, new_cards):
        if not isinstance(new_cards, list):
            raise TypeError

        for i in range(1, self.pile_count + 1):
            self.card_piles.append(new_cards[:i])
            del new_cards[:i]

        self.spit_pile = new_cards

    def PrintCards(self):

        print(colored(f"\t\t\t{self.name}".center(50), self.font_color, attrs=["reverse", "bold"]))

        pile_row = ""
        x = 0

        for pile in self.card_piles:
            pile_row += f"{pile[0] if len(pile) > 0 else ' '} ({len(pile)})\t"
            x += 1

        print(colored(pile_row, self.color, attrs=["bold"]))

    def PrintCards2(self):

        print(colored(f"{self.name}".center(50), self.color, attrs=["reverse", "bold"]))

        row1 = "┌─┐  " * self.pile_count
        row2 = ""
        row3 = ""
        for pile in self.card_piles:
            character = getFirst(pile, '░')
            row2 += f"│{character}│  "
            row3 += f"└─┘  "

        print(colored(row1.center(50), self.color, attrs=["bold"]))
        print(colored(row2.center(50), self.color, attrs=["bold"]))
        print(colored(row3.center(50), self.color, attrs=["bold"]))

    def HasNoCards(self):
        return sum(len(pile) for pile in self.card_piles) == 0

    def GetFrontCards(self, omit_empty_piles= False, default_if_empty_pile= ' '):
        if omit_empty_piles:
            result = []
            for pile in self.card_piles:
                if len(pile) > 0:
                    result.append(pile[0])
            return result
        else:
            return [getFirst(i, default_if_empty_pile) for i in self.card_piles]

    def MoveCards(self):

        while True:
            card = self.ConvertCardToNumber(self.GetInput(colored(f"{self.name}, choose card: ", self.color, attrs=["bold", "reverse"])))

            available_cards = [getFirst(i) for i in self.card_piles]
            print(available_cards)

            if card in available_cards:
                pile_index = available_cards.index(card)
                print(f"{self.name} chose {card} - value: {self.ConvertCardToNumber(card)} from pile {pile_index + 1}")
                del self.card_piles[pile_index][0]  # REDRAW?
                return card
            else:
                print("Invalid card. Try again.")

    def ConvertCardToNumber(self, card):

        if not (isinstance(card, str) or not isinstance(card, int)):
            raise TypeError

        card_value = tryConvertToInt(card)

        if not card_value:
            if card_value in self.faceValues:
                return self.faceValues[card_value]
            else:
                print(f"Type : {type(card_value)} Value: {card_value}")
                raise ValueError
        else:
            return card_value

    def MoveDuplicatesToLeft(self):
        front_cards = self.GetFrontCards(default_if_empty_pile=0)



    def MoveCardToEmptySpots(self):
        pass
