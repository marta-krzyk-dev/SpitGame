from termcolor import colored
from Project4_Split.helpers import getFirst, tryConvertToInt, getFirstElements
from Project4_Split.Deck import Deck
from Project4_Split.Player import Player
from Project4_Split.ConsoleInputOutputManipulator import ConsoleInputOutputManipulator

class SpitGame(ConsoleInputOutputManipulator):
    def __init__(self, pile_count = 5):

        self.pile_count = pile_count
        self.current_player = None
        self.faceValues = {
            "A" : 14,
            "K" : 13,
            "Q" : 12,
            "J" : 11
        }
        self.pile_names = {
             0 : 'Q',
             1 : 'W',
             2 : 'E',
             3 : 'R',
             4 : 'T'
        }
        self.CreatePlayers()

    def Play(self):

        while True:
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            self.PrintGame()

            current_player_can_move = self.CanMoveCards(self.current_player)
            other_player = self.player2 if self.current_player == self.player1 else self.player1
            other_player_can_move = self.CanMoveCards(other_player)

            if not current_player_can_move and other_player_can_move:
                print(colored(f"{self.current_player.name}, you cannot move a card. You lose a round!", self.current_player.color, attrs=["bold", "reverse"]))
                continue
            elif not current_player_can_move and not other_player_can_move:
                # Each player can place 1 card onto their spits
                self.Print(f"{self.current_player.name}, {other_player.name}, you both cannot move any cards. Choose a card to be placed onto your respective spit pile.")

            self.current_player.MoveDuplicatesToLeft()
            self.current_player.MoveCardToEmptySpots()

            self.MoveCards(self.current_player)
            if self.current_player.HasNoCards():
                print(f"{self.current_player.name} WON!")
                break
            elif self.Draw():
                print(f"DRAW!")

    def CreatePlayers(self):
        name1 = "Dolphin"  # AskForName("Player 1")
        name2 = "Parrot"  # AskForName("Player 2")

        deck = Deck()
        half1, half2 = deck.getHalves()

        self.player1 = Player(name1, half1, self.pile_count, self.pile_names, "green")
        self.player2 = Player(name2, half2, self.pile_count, self.pile_names, "magenta")

        self.current_player == self.player1


    def PrintTitle(self):
        print("***  SPIT GAME  ***")


    def AskForName(self, playerName):
        while True:
            name = input(f"{playerName} Enter your name >>")

            if len(name) > 0:
                if self.IsCommand(name):
                    self.Command(name)
                else:
                    return name

    def MoveCards(self, player):

        while True:
            pile_card = input(colored(f"{player.name}, choose a card: ", player.color, attrs=["bold","reverse"])).upper()

            if self.IsCommand(pile_card):
                self.Command(pile_card)
                continue

            available_cards = player.GetFrontCards()

            if pile_card in available_cards:
                pile_index = available_cards.index(pile_card)
                print(f"{player.name} chose {pile_card} of value {self.ConvertCardToNumericValue(pile_card)}")
                #del player.card_piles[pile_index][0]  # REDRAW?

                isValidPair1 = self.IsValidPair(pile_card, self.player1.spit_pile[0])
                isValidPair2 = self.IsValidPair(pile_card, self.player2.spit_pile[0])

                if isValidPair1 and not isValidPair2:
                    self.player1.spit_pile.insert(0, pile_card)
                    break

                elif isValidPair2 and not isValidPair1:
                    self.player2.spit_pile.insert(0, pile_card)
                    break

                elif isValidPair1 and isValidPair2:
                    while True:
                        split_pile_number = tryConvertToInt(input(f"{player.name}, choose spit pile to add your {pile_card} card: "))
                        if split_pile_number == 1:
                            self.player1.spit_pile.insert(0, pile_card)
                            break
                        elif split_pile_number == 2:
                            self.player2.spit_pile.insert(0, pile_card)
                            break
                        else:
                            print("Invalid pile. Try again.")
            else:
                print(f"Invalid card {pile_card} type {type(pile_card)} avaialble {available_cards}. Try again.")

        del player.card_piles[pile_index][0]  # REDRAW?


    def IsValidPair(self, card1, card2):

         card1 = self.ConvertCardToNumericValue(card1)
         card2 = self.ConvertCardToNumericValue(card2)
         diff = abs(card1 - card2)

         return diff < 2 or diff == 12 # Cards have 0, 1 or 12 value difference. (one card is 2, the other is A)

    def ConvertCardToNumericValue(self, card):

        if not (isinstance(card, str) or isinstance(card, int)):
            raise TypeError

        card_as_number = tryConvertToInt(card)

        if not card_as_number:
            if card in self.faceValues:
                return self.faceValues[card]
            else:
                raise ValueError
        else:
            return card_as_number

    def Draw(self):
        return False

    def PrintGame(self):
        #self.player1.PrintCards2()
        self.PrintCards2(self.player1.GetFrontCards(), self.player1.color)
        self.PrintCards2([getFirst(self.player1.spit_pile), getFirst(self.player2.spit_pile)])
       # print(f"{getFirst(self.player1.spit_pile)} {getFirst(self.player2.spit_pile)}".center(50))
        self.PrintCards2(self.player2.GetFrontCards(), self.player2.color)

    def PrintCards2(self, cards, color="white"):

        row1 = "┌──┐  " * len(cards)
        row2 = ""
        row3 = ""
        for card in cards:
            character = '░░' if str(card).strip() == "" else card
            row2 += f"│{character.ljust(2)}│  "
            row3 += f"└──┘  "

        print(colored(row1.center(50), color, attrs=["bold"]))
        print(colored(row2.center(50), color, attrs=["bold"]))
        print(colored(row3.center(50), color, attrs=["bold"]))

    def CanMoveCards(self, player):
        spits = getFirstElements(self.player1.spit_pile, self.player2.spit_pile)

        player_cards = player.GetFrontCards(omit_empty_piles=True)

        for card in player_cards:
            for spit in spits:
                if self.IsValidPair(card, spit):
                    return True # There is at least 1 pair

        return False








