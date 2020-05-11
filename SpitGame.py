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
        self.round_number = 0
    # endregion

    # region Main methods
    def PlayGame(self):

        self.round_number = 0
        end = False

        while end is False:
            end = self.PlayRound()
            self.PrintScores()

        self.Print('END OF THE GAME')

    def PlayRound(self):
        self.round_number += 1
        self.PrintRound()
        turns_without_spit_move = 0

        while True:
            self.ChangePlayer()
            self.PrintGame()

            spit_cards = getFirstElements(self.current_player.spit_pile, self.other_player.spit_pile)
            current_player_can_move = self.current_player.CanMakeAnyMove(spit_cards)
            other_player_can_move = self.other_player.CanMakeAnyMove(spit_cards)

            if (turns_without_spit_move > 2) or (not current_player_can_move and not other_player_can_move):
                self.Draw()
                return False
            elif not current_player_can_move and other_player_can_move:
                self.current_player.PrintReverse(f"{self.current_player.name}, you cannot move a card. You lose a turn!")
                continue

            fewer_cards_than_piles = self.current_player.GetPileCardCount() <= self.pile_count
            if not fewer_cards_than_piles:
                self.MoveCardsInPlayersPile(self.current_player) # Move duplicates and fill empty spots

            if self.current_player.HasValidPairs(spit_cards):
                turns_without_spit_move = 0
                self.AddCardToSpitPile(self.current_player)
            else:
                turns_without_spit_move += 1
                self.current_player.PrintReverse(f"{self.current_player.name}, you don't have a valid pair to add to any spit pile. End of turn for you!")

            if self.current_player.HasNoCards():
                self.GameWin(winner=self.current_player)
                return True
            elif self.current_player.HasNoCardsInPiles():
                self.RoundWin(winner=self.current_player, loser=self.other_player)
                return False

    def GameWin(self, winner):
        winner.PrintReverse(f"{winner.name}, YOU THE GAME after {self.round_number} round{'' if self.round_number == 1 else 's'}!")
        winner.AddToScore()

    def RoundWin(self, winner, loser):
        winner.PrintReverse(f"{winner.name}, YOU WON ROUND {self.round_number}!")
        loser.PrintReverse(f"{loser.name}, YOU LOST ROUND {self.round_number}!")

        winner.AddToScore()

        spit1, spit2 = self.ChooseSpits(choosing_player=winner)
        winner.ShuffleCards(spit1)
        loser.ShuffleCards(spit2)

        winner.PrintReverse(f"{winner.name}, spit pile with {len(spit1)} cards was added to your cards and reshuffled.")
        loser.PrintReverse(f"{loser.name}, spit pile with {len(spit2)} cards was added to your cards and reshuffled.")

    def Draw(self):
        self.Print(f"{self.current_player.name}, {self.other_player.name}, you both cannot move any cards, this is end of round {self.round_number}.")
        spit1 = self.current_player.spit_pile
        spit2 = self.other_player.spit_pile
        self.current_player.ShuffleCards(spit1)
        self.other_player.ShuffleCards(spit2)
        self.current_player.Print(
            f"{self.current_player.name}, spit pile with {len(spit1)} cards was added to your cards and reshuffled.")
        self.other_player.Print(
            f"{self.other_player.name}, spit pile with {len(spit2)} cards was added to your cards and reshuffled.")
    # endregion

    # region Helper methods
    def ChooseSpits(self, choosing_player):
        answer = self.GetInput(f"{choosing_player.name}, choose spit pile 1 ({len(self.player1.spit_pile)} cards) or spit pile 2 ({len(self.player2.spit_pile)} cards) to add to your cards (type 1 or 2):", ['1', '2'])

        if answer == '1':
            return self.player1.spit_pile, self.player2.spit_pile
        else:
            return self.player2.spit_pile, self.player1.spit_pile

    def CreatePlayers(self, ask_for_names=True):

        if ask_for_names:
            name1 = self.AskForName("Player 1")
            name2 = self.AskForName("Player 2", [name1])
        else:
            name1 = "Dolphin"
            name2 = "Parrot"

        deck = Deck()
        half1, half2 = deck.getHalves()

        self.player1 = Player(name1, half1, self.pile_count, "green")
        self.player2 = Player(name2, half2, self.pile_count, "magenta")

        self.current_player == self.player1

    def AskForName(self, temporary_player_name, existing_names=[], max_len=15):
        while True:
            name = self.GetInput(f"{temporary_player_name}, enter your name >>").strip()

            if len(name) > 0:
                if name in existing_names:
                    self.Print("Player with that name already exists.")
                else:
                    return name[:int(max_len)]

    def AddCardToSpitPile(self, player):

        if player.HasNoCardsInPiles():
            return

        while True:
            pile_card, pile_index = player.ChooseCard()

            isValidPair1 = IsValidPair(pile_card, self.player1.spit_pile[0]) if len(self.player1.spit_pile) > 0 else False
            isValidPair2 = IsValidPair(pile_card, self.player2.spit_pile[0]) if len(self.player2.spit_pile) > 0 else False

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

        del player.card_piles[pile_index][0]

    def ChangePlayer(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def MoveCardsInPlayersPile(self, player):

        duplicates = player.GetDuplicateIndexes()
        old_duplicates = []
        while True:
            if len(duplicates) > 0:
                _, rejected_duplicates = player.MoveDuplicatesToLeft(duplicates)
                old_duplicates += rejected_duplicates
                self.PrintGame()

            while True:
                if player.CanMoveCardToEmptySpot():
                    player.MoveCardsToEmptySpots()
                    self.PrintGame()
                else:
                    break

            # Check again for duplicates after moving cards to empty spots
            new_duplicates = [i for i in player.GetDuplicateIndexes() if i not in old_duplicates]
            if len(new_duplicates) > 0:
                duplicates = new_duplicates

            else:
                return
    # endregion

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
        art = f"\
                                              $$\ \n\
                                              $$ |		.------.\n\
 $$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$\   $$$$$$$ |		| {str(self.round_number).ljust(2, ' ')}   |\n\
$$  __$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$ |		| :##: |\n\
$$ |  \__|$$ /  $$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |		| :##: |\n\
$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |		|   {str(self.round_number).rjust(2, ' ')} |\n\
$$ |      \$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$ |		.------.\n\
\__|       \______/  \______/ \__|  \__| \_______|\n\
"
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
