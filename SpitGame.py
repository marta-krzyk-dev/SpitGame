from termcolor import colored
from Project4_Split.helpers import getFirst, tryConvertToInt, getFirstElements
from Project4_Split.Deck import Deck
from Project4_Split.Player import Player
from Project4_Split.ConsoleInputOutputManipulator import ConsoleInputOutputManipulator
from Project4_Split.card_helpers import IsValidPair


class SpitGame(ConsoleInputOutputManipulator):
    # region Constructor
    def __init__(self, pile_count=5):
        ConsoleInputOutputManipulator.__init__(self, font_color="cyan")

        self.pile_count = pile_count
        self.current_player = None
        self.other_player = None
        self.round_number = 1
    # endregion

    def PlayRound(self):

        self.PrintRound()
        self.PrintScores()
        self.round_number += 1

        while True:

            self.ChangePlayer()
            #self.current_player.AdjustCardsForTesting()

            self.PrintGame()

            spit_cards = getFirstElements(self.current_player.spit_pile, self.other_player.spit_pile)
            current_player_can_move = self.current_player.CanMakeAnyMove(spit_cards)
            other_player_can_move = self.other_player.CanMakeAnyMove(spit_cards)

            if not current_player_can_move and other_player_can_move:
                self.current_player.PrintReverse(f"{self.current_player.name}, you cannot move a card. You lose a round!")
                continue
            elif not current_player_can_move and not other_player_can_move:
                # Each player can place 1 card onto their spits
                self.Print(f"{self.current_player.name}, {self.other_player.name}, you both cannot move any cards. Choose a card to be placed onto your respective spit pile.")
                self.current_player.MoveAnyCardToSpitPile()
                self.other_player.MoveAnyCardToSpitPile()
                self.ChangePlayer()  # Stay with the same player for the next round
                continue

            self.MoveCardsInPlayersPile(self.current_player) # Move duplicates and fill empty spots

            if self.current_player.HasValidPairs(spit_cards):
                self.MoveCards(self.current_player)

            if self.current_player.HasNoCards():
                spit1, spit2 = self.ChooseSpits(self.current_player)
                self.current_player.ShuffleCards(spit1)
                self.other_player.ShuffleCards(spit2)
                self.current_player.Print(f"{self.current_player.name}, spit pile with {len(spit1)} cards {spit1} was added to your cards.")
                self.other_player.Print(f"{self.other_player.name}, spit pile with {len(spit2)} cards {spit2} was added to your cards.")
                print(f"{self.current_player.name} WON ROUND {self.round_number}!")
                break
            elif self.Draw():
                print(f"DRAW!")

    def ChooseSpits(self, choosing_player):
        answer = self.GetInputWithAllowedAnswers(f"{choosing_player.name}, choose spit pile to add to your cards (type 1 or 2):", ['1', '2'])

        if answer == '1':
            return self.player1.spit_pile, self.player2.spit_pile
        else:
            return self.player2.spit_pile, self.player1.spit_pile

    def CreatePlayers(self, use_defaults=False):

        if use_defaults:
            name1 = "Dolphin"
            name2 = "Parrot"
        else:
            name1 = self.AskForName("Player 1")
            name2 = self.AskForName("Player 2", [name1])

        deck = Deck()
        half1, half2 = deck.getHalves()

        self.player1 = Player(name1, half1, self.pile_count, "green")
        self.player2 = Player(name2, half2, self.pile_count, "magenta")

        self.current_player == self.player1

    def AskForName(self, temporary_player_name, existing_names=[], max_len=15):
        while True:
            name = self.GetInput(f"{temporary_player_name}, enter your name >>").strip()

            if self.IsCommand(name):
                continue

            if len(name) > 0:
                if name in existing_names:
                    self.Print("Player with that name already exists.")
                else:
                    return name[:int(max_len)]

    def MoveCards(self, player):

        if player.HasNoCards():
            return

        while True:
            pile_card, pile_index = player.ChooseCard()

            isValidPair1 = IsValidPair(pile_card, self.player1.spit_pile[0])
            isValidPair2 = IsValidPair(pile_card, self.player2.spit_pile[0])

            if isValidPair1 and not isValidPair2:
                self.player1.spit_pile.insert(0, pile_card)
                break

            elif isValidPair2 and not isValidPair1:
                self.player2.spit_pile.insert(0, pile_card)
                break

            elif not isValidPair1 and not isValidPair2:
                print(f"{pile_card} doesn't make a valid pair.")
                continue

            else:  # isValidPair1 and isValidPair2:
                self.player1.spit_pile.insert(0, pile_card)
                break

        # print(f"Removing card {player.card_piles[pile_index][0]} from pile {pile_index}")
        del player.card_piles[pile_index][0]

    def Draw(self):
        return False

    def ChangePlayer(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def ChooseSpit(self, player):
        split_pile_number = tryConvertToInt(input(f"{player.name}, choose spit pile to add your cards (1 or 2): "))
        if split_pile_number == 1:
            return self.player1.spit_pile, self.player2.spit_pile
        elif split_pile_number == 2:
            return self.player2.spit_pile, self.player1.spit_pile
        else:
            print("Invalid pile. Try again.")

    def MoveCardsInPlayersPile(self, player):

        duplicates = player.GetDuplicateIndexes()
        print(f'Here are duplicates: {duplicates}')
        while True:
            if len(duplicates) > 0:
                player.MoveDuplicatesToLeft(duplicates)
                self.PrintGame()

            while True:
                if player.CanMoveCardToEmptySpot():
                    player.MoveCardsToEmptySpots()
                    self.PrintGame()
                else:
                    break

            # Check again for duplicates after moving cards to empty spots
            new_duplicates = [i for i in player.GetDuplicateIndexes() if i not in duplicates]
            if len(new_duplicates) > 0:
                duplicates = new_duplicates
                #TODO remove log
                print(f'There are new duplicates: {duplicates}')
            else:
                return

    # region Print methods
    def PrintTitle(self):
        try:
            with open("cards_art.txt", "r") as file:
                art = file.read()
                print(colored(f"{art}".center(50), "cyan", attrs=["bold"]))
        except FileNotFoundError:
            print(colored(f"***  SPIT GAME  ***".center(50), "cyan", attrs=["bold", "reverse"]))

    def PrintScores(self):

        max_name_len = 15
        score_len = 5
        result_len = 7

        result1, result2 = self.GetScoreResults(self.player1.score, self.player2.score)
        row1 = f"{self.player1.name[:max_name_len].ljust(max_name_len)} ║ {str(self.player1.score).center(score_len)} ║ {result1.ljust(result_len)}"
        row2 = f"{self.player2.name[:max_name_len].ljust(max_name_len)} ║ {str(self.player2.score).center(score_len)} ║ {result2.ljust(result_len)}"

        self.Print("╔═" + "═" * max_name_len + "═╦═" + ("═" * score_len) + "═╦═" + ("═" * result_len) + "═╗")
        self.Print(f"║ {'PLAYER'.center(max_name_len)} ║ SCORE ║ {'RESULT'.ljust(result_len)} ║")
        self.Print("╠═" + "═" * max_name_len + "═╬═" + ("═" * score_len) + "═╬═" + ("═" * result_len) + "═╣")
        self.Print(f"║ {row1} ║")
        self.Print(f"║ {row2} ║")
        self.Print("╚═" + "═" * max_name_len + "═╩═" + ("═" * score_len) + "═╩═" + ("═" * result_len) + "═╝")

    def PrintGame(self):
        # self.ClearConsole()
        print()
        self.player1.PrintCards(print_name_above_cards=True)
        self.PrintStacks([self.player1.spit_pile, self.player2.spit_pile], self.player1.font_color,
                         self.player2.font_color)
        self.player2.PrintCards(print_name_above_cards=False)
        print()

    def PrintStacks(self, card_piles, arrow_color1, arrow_color2, print_size_above_cards=False,
                    print_size_below_cards=False):

        row_arrow_above = f" ▼          "  # f"[{len(card_piles[0])}]  ▼          "
        row1 = ""
        row2 = ""
        row3 = ""
        row_arrow_below = f"       ▲"  # [{len(card_piles[1])}]"
        pile_sizes_row = ""

        for pile in card_piles:
            row1 += "┌──┐  " if len(pile) < 2 else "╔══╗  "
            character = getFirst(pile, '░')
            row2 += f"│{character.ljust(2)}│  " if len(pile) < 2 else f"║{character.ljust(2)}║  "
            row3 += "└──┘  " if len(pile) < 2 else "╚══╝  "
            pile_sizes_row += f"[{str(len(pile))}]".rjust(4) + "  "

        if print_size_above_cards:
            self.Print(pile_sizes_row.center(50))

        self.Print(row_arrow_above.center(50), arrow_color1)
        self.Print(row1.center(50))
        self.Print(row2.center(50))
        self.Print(row3.center(50))
        self.Print(row_arrow_below.center(50), arrow_color2)

        if print_size_below_cards:
            self.Print(pile_sizes_row.center(50))

    def PrintSpitPiles(self, cards, color="white"):

        row0 = "  ▼"
        row1 = "┌──┐  " * len(cards)
        row2 = ""
        row3 = ""
        row4 = ""
        row5 = "▲"

        for card in cards:
            character = '░░' if str(card).strip() == "" else card
            row2 += f"│{character.ljust(2)}│  "
            row3 += f"└──┘  "
            row4 += f" "

        self.PrintCentered(row0)
        print(colored(row1.center(50), color, attrs=["bold"]))
        print(colored(row2.center(50), color, attrs=["bold"]))
        print(colored(row3.center(50), color, attrs=["bold"]))
        self.PrintCentered(row5)

    def PrintRound(self):
        art = f"\n\
  ^    ^    ^    ^    ^    ^  \n\
 / \  / \  / \  / \  / \  / \ \n\
<_R_><_O_><_U_><_N_><_D_><{str(self.round_number).center(3, '_')}>"

        self.PrintCentered(art)

    def GetScoreResults(self, score1, score2):
        try:
            if score1 == score2:
                return 'DRAW', 'DRAW'
            elif score1 < score2:
                return 'LOOSING', 'WINNING'
            else:
                return 'WINNING', 'LOOSING'
        except TypeError:
            return 'UNKNOWN', 'UNKNOWN'

    # endregion