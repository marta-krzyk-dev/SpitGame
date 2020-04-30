import termcolor
from termcolor import colored
from Project4_Split.helpers import getFirst, tryConvertToInt
from Project4_Split.ConsoleInputOutputManipulator import ConsoleInputOutputManipulator
from random import shuffle
from Project4_Split.card_helpers import ThereAreValidPairs, IsValidPair


class Player(ConsoleInputOutputManipulator):
    def __init__(self, name, cards, pile_count, color="green"):

        ConsoleInputOutputManipulator.__init__(self, color)

        self.card_piles = []
        self.spit_pile = []
        self.pile_count = pile_count
        self.name = name
        self.color = color if color in termcolor.COLORS.keys() else "green"
        self.score = 0

        self.ArrangeCards(cards)

    def AddToScore(self):
        self.score += 1

    def PrintCardsX(self):
        for pile in self.card_piles:
            print(pile)

    def ShuffleCards(self, new_cards):
        pile_cards = [x for sublist in self.card_piles for x in sublist]
        all_cards = pile_cards + new_cards
        shuffle(all_cards)

        self.ArrangeCards(all_cards)

    def ArrangeCards(self, new_cards):
        if not isinstance(new_cards, list):
            raise TypeError

        self.card_piles = []
        for i in range(self.pile_count):
            self.card_piles.append([])

        begin = 0
        card_count = len(new_cards)

        # Arrange cardss into piles, like so:
        '''
        1
        2 6
        3 7 10
        4 8 11 13
        5 9 12 14 15 
        '''
        for y in range(self.pile_count):
            for x in range(begin, self.pile_count):
                self.card_piles[x].append(new_cards[0])
                del new_cards[0]
                card_count -= 1
                if card_count == 0:
                    break
            begin += 1

        # Put the rest of the cards into spit pile
        self.spit_pile = new_cards

        # print(f"Rearranged cards: {self.card_piles}")
        # print(f"SPIT: {self.spit_pile}")

    def ChooseCard(self, message=""):

        available_cards = self.GetFrontCards()

        while True:
            pile_card = self.GetInput(colored(f"{self.name}, choose a card: " if message is "" else message, self.color, attrs=["bold", "reverse"])).upper()

            if self.IsCommand(pile_card) or pile_card.strip() == "":
                continue

            if pile_card in available_cards:
                return pile_card, available_cards.index(pile_card)
            else:
                print(f"Invalid card. Try again.")

    def PrintCards(self, print_name_above_cards= True):

        row1 = ""
        row2 = ""
        row3 = ""
        pile_sizes_row = ""
        for pile in self.card_piles:
            row1 += "┌──┐  " if len(pile) < 2 else "╔══╗  "
            character = getFirst(pile, '░')
            row2 += f"│{character.ljust(2)}│  " if len(pile) < 2 else f"║{character.ljust(2)}║  "
            row3 += "└──┘  " if len(pile) < 2 else "╚══╝  "
            pile_sizes_row += f"[{str(len(pile))}]".rjust(4) + "  " if len(pile) > 1 else " " * 6

        if print_name_above_cards:
            self.PrintReverse(f"{self.name}".center(50))
            self.Print(pile_sizes_row.center(50))

        self.Print(row1.center(50))
        self.Print(row2.center(50))
        self.Print(row3.center(50))

        if not print_name_above_cards:
            self.Print(pile_sizes_row.center(50))
            self.PrintReverse(f"{self.name}".center(50))

    def HasNoCards(self):
        return sum(len(pile) for pile in self.card_piles) == 0

    def GetCardCount(self):
        return sum(len(pile) for pile in self.card_piles)

    def GetFrontCards(self, omit_empty_piles=False, default_if_empty_pile=' '):
        if omit_empty_piles:
            result = []
            for pile in self.card_piles:
                if len(pile) > 0:
                    result.append(pile[0])
            return result
        else:
            return [getFirst(i, default_if_empty_pile) for i in self.card_piles]

    def GetCard(self):

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

    def HasDuplicates(self):
        front_cards = self.GetFrontCards(omit_empty_piles=True)
        unique_front_cards = set(front_cards)

        return len(front_cards) != len(unique_front_cards)

    def MoveFirstDuplicateToLeft(self):
        front_cards = self.GetFrontCards(omit_empty_piles=True)

        index: int = 0
        max = len(front_cards) - 1

        while index < max:
            card = front_cards[index]
            #print(f"Looking for {card} {type(card)} in {front_cards[(index + 1):]}")
            if card in front_cards[(index + 1):]:
                second_index = front_cards[index + 1:].index(card) + index + 1
                #print(f"Found duplicate {card} at {second_index}")

                while True:
                    answer = self.GetInput(f"{self.name}, do you want to stack duplicate card {card} from #{second_index + 1} to #{index + 1} pile? (y/n)").strip()
                    if self.IsCommand(answer) or len(answer) == 0:
                        continue
                    elif answer.startswith('y') or answer.startswith('n'):
                        break

                if answer.startswith('y'):
                    del self.card_piles[second_index][0]
                    self.card_piles[index].insert(0, card)
                break

            index += 1

    def MoveAnyCardToSpitPile(self):
        card, pile_index = self.ChooseCard()
        del self.card_piles[pile_index][0]
        self.spit_pile.insert(0, card)

    def CanMakeAMove(self, spit_cards):
        return ThereAreValidPairs(spit_cards, self.GetFrontCards(omit_empty_piles=True)) or self.HasDuplicates() or self.CanMoveCardToEmptySpot()

    def CanMoveCardToEmptySpot(self):

        if self.GetCardCount() <= self.pile_count:
            return False, []

        empty_spot_indexes = []
        can_move = False
        has_empty_pile = False

        index = 0
        for pile in self.card_piles:
           if len(pile) > 1:
               can_move = True
           elif len(pile) == 0:
               has_empty_pile = True
               empty_spot_indexes.append(index)

           index += 1

        return (can_move and has_empty_pile), empty_spot_indexes

    def MoveCardsToEmptySpots(self, empty_indexes):

        for empty_index in empty_indexes:
            card, move_index = self.ChooseCard(message=f"Choose card to move to the empty pile #{empty_index + 1}")
            self.MoveCard(move_index, empty_index)

    def MoveCard(self, from_pile_index, to_pile_index):
        try:
            temp = self.card_piles[from_pile_index][0]
            del self.card_piles[from_pile_index][0]
            self.card_piles[to_pile_index].insert(0, temp)
        except IndexError:
            pass