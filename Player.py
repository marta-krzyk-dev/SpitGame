from termcolor import colored, COLORS
from Project4_Split.CardPrinter import CardPrinter
from Project4_Split.helpers import getFirst
from Project4_Split.InputManipulator import InputManipulator
from random import shuffle
from Project4_Split.card_helpers import ThereAreValidPairs, ConvertCardToNumericValue


class Player(InputManipulator, CardPrinter):
    #region Constructor
    def __init__(self, name, cards, pile_count, color="green"):

        InputManipulator.__init__(self, color)
        CardPrinter.__init__(self, color)

        self.card_piles = []
        self.spit_pile = []
        self.pile_count = pile_count
        self.name = name
        self.color = color if color in COLORS.keys() else "green"
        self.score = 0

        self.ArrangeCardsIntoPiles(cards)
    #endregion

    def AddToScore(self):
        self.score += 1

    def ShuffleCards(self, new_cards):
        pile_cards = [x for sublist in self.card_piles for x in sublist]
        all_cards = pile_cards + new_cards
        shuffle(all_cards)

        self.ArrangeCardsIntoPiles(all_cards)

    def ArrangeCardsIntoPiles(self, cards):
        if not isinstance(cards, list):
            raise TypeError

        self.card_piles = []
        for i in range(self.pile_count):
            self.card_piles.append([])

        begin = 0
        card_count = len(cards)

        # Arrange cards into piles, like so:
        '''
        1
        2 6
        3 7 10
        4 8 11 13
        5 9 12 14 15 
        '''
        try:
            for y in range(self.pile_count):
                for x in range(begin, self.pile_count):
                    self.card_piles[x].append(cards[0])
                    del cards[0]
                    card_count -= 1
                    if card_count == 0:
                        break
                begin += 1
        except IndexError:
            pass
        # Put the rest of the cards into spit pile
        self.spit_pile = cards

    def ChooseCard(self, message=None, skip_phrase=None):

        available_cards = self.GetFrontCards(omit_empty_piles=True)

        while True:
            pile_card = self.GetInput(
                colored(f"{self.name}, choose a card: " if message is None else message, self.color,
                        attrs=["bold", "reverse"])).upper()

            if isinstance(skip_phrase, str) and pile_card.strip().upper() == skip_phrase.strip().upper():
                return None, None
            elif self.IsCommand(pile_card) or pile_card.strip() == "":
                continue

            if pile_card in available_cards:
                return pile_card, self.GetFrontCards(omit_empty_piles=False).index(pile_card)
            else:
                print(f"Invalid card. Try again.")

    def HasNoCards(self):
        return len(self.spit_pile) == 0 and self.HasNoCardsInPiles()

    def HasNoCardsInPiles(self):
        return sum(len(pile) for pile in self.card_piles) == 0

    def GetPileCardCount(self):
        return sum(len(pile) for pile in self.card_piles)

    def GetFrontCards(self, omit_empty_piles=False, default_if_empty_pile=' '):
        if omit_empty_piles:
            return [pile[0] for pile in self.card_piles if len(pile) > 0]
        else:
            return [getFirst(i, default_if_empty_pile) for i in self.card_piles]

    def GetCard(self):

        while True:
            card = ConvertCardToNumericValue(
                self.GetInput(colored(f"{self.name}, choose card: ", self.color, attrs=["bold", "reverse"])))

            available_cards = [getFirst(i) for i in self.card_piles]
            print(available_cards)

            if card in available_cards:
                pile_index = available_cards.index(card)
                print(f"{self.name} chose {card} - value: {ConvertCardToNumericValue(card)} from pile {pile_index + 1}")
                del self.card_piles[pile_index][0]  # REDRAW?
                return card
            else:
                print("Invalid card. Try again.")

    # region Duplicates logic
    def HasDuplicates(self):
        front_cards = self.GetFrontCards(omit_empty_piles=True)
        unique_front_cards = set(front_cards)

        return len(front_cards) != len(unique_front_cards)

    def GetDuplicateIndexes(self):
        front_cards = self.GetFrontCards(omit_empty_piles=False)
        duplicate_indexes = []

        for c in front_cards:
            if c == ' ':
                continue
            indexes = [i for i in range(len(front_cards)) if front_cards[i] == c]
            if len(indexes) > 1 and indexes not in duplicate_indexes:
                duplicate_indexes.append(indexes)

        return duplicate_indexes

    def MoveDuplicatesToLeft(self, duplicate_indexes):

        front_cards = self.GetFrontCards(omit_empty_piles=False)
        removed_duplicates = []
        rejected_duplicates = []

        for indexes in duplicate_indexes:
            left_most_index = indexes[0]
            card = front_cards[left_most_index]

            for duplicate_index in indexes[1:]:
                while True:
                    answer = self.GetInput(
                        f"{self.name}, do you want to stack duplicate card {card} from #{duplicate_index + 1} to #{left_most_index + 1} pile? (y/n)",
                        allowed_answers=['y', 'n']).strip()
                    if self.IsCommand(answer) or len(answer) == 0:
                        continue
                    elif answer.startswith('y') or answer.startswith('n'):
                        break

                if answer.startswith('y'):
                    removed_duplicates.append([left_most_index, duplicate_index])
                    del self.card_piles[duplicate_index][0]
                    self.card_piles[left_most_index].insert(0, card)
                else:
                    rejected_duplicates.append([left_most_index, duplicate_index])

        return removed_duplicates, rejected_duplicates
    # endregion

    def MoveAnyCardToSpitPile(self):
        card, pile_index = self.ChooseCard()
        del self.card_piles[pile_index][0]
        self.spit_pile.insert(0, card)

    def HasValidPairs(self, spit_cards):
        return ThereAreValidPairs(spit_cards, self.GetFrontCards(omit_empty_piles=True))

    def CanMakeAnyMove(self, spit_cards):
        return self.HasValidPairs(spit_cards) or self.HasDuplicates() or self.CanMoveCardToEmptySpot()

    # region Empty spot logic
    def CanMoveCardToEmptySpot(self):

        if self.GetPileCardCount() < self.pile_count:
            return True

        can_move = False
        has_empty_pile = False

        index = 0
        for pile in self.card_piles:
            if len(pile) > 1:
                can_move = True
            elif len(pile) == 0:
                has_empty_pile = True
            index += 1

        return can_move and has_empty_pile

    def GetEmptyIndexes(self):

        if self.GetPileCardCount() <= self.pile_count:
            return []

        empty_spot_indexes = []
        index = 0

        for pile in self.card_piles:
            if len(pile) == 0:
                empty_spot_indexes.append(index)
            index += 1

        return empty_spot_indexes

    def MoveCardsToEmptySpots(self):

        empty_indexes = self.GetEmptyIndexes()

        for empty_index in empty_indexes:
            card, move_index = self.ChooseCard(
                message=f"Choose card to move to the empty pile #{empty_index + 1} or type n to skip", skip_phrase='n')
            self.MoveCard(move_index, empty_index)

    def MoveCard(self, from_pile_index, to_pile_index):
        try:
            temp = self.card_piles[from_pile_index][0]
            del self.card_piles[from_pile_index][0]
            self.card_piles[to_pile_index].insert(0, temp)
        except IndexError:
            pass
    # endregion

    # region Print methods
    def PrintCards(self, print_name_above_cards=False, print_name_below_cards=False):

        if print_name_above_cards:
            self.PrintReverse(f"{self.name}".center(50))

        self.PrintCardPiles(self.card_piles, print_size_above_cards=print_name_above_cards, print_size_below_cards=print_name_below_cards)

        if print_name_below_cards:
            self.PrintReverse(f"{self.name}".center(50))
    # endregion

    def AdjustCardsForTesting(self):
        self.card_piles[0] = ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2']
        self.card_piles[1] = ['9']
        self.card_piles[2] = ['9']
        self.card_piles[3] = ['Q']
        self.card_piles[4] = ['K']
        self.spit_pile = ['2', '2']

    def AdjustCardsForTestingDolphin(self):
        self.card_piles[0] = ['A','4']
        self.card_piles[1] = []
        self.card_piles[2] = ['J', 'J']
        self.card_piles[3] = ['J']
        self.card_piles[4] = ['K']
        self.spit_pile = ['6', '2']

    def AdjustCardsForTestingParrot(self):
        self.card_piles[0] = []
        self.card_piles[1] = ['3']
        self.card_piles[2] = ['Q', 'Q']
        self.card_piles[3] = ['J','J','J']
        self.card_piles[4] = ['A']
        self.spit_pile = ['5', '2']

    def AdjustCardsForTesting_WIn(self):
        self.card_piles[0] = []
        self.card_piles[1] = []
        self.card_piles[2] = ['Q', 'Q']
        self.card_piles[3] = []
        self.card_piles[4] = []
        self.spit_pile = []

    def AdjustCardsForTesting_WIn2(self):

        self.spit_pile = ['Q']

