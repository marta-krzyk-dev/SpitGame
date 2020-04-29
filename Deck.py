<<<<<<< HEAD
from random import shuffle

class Deck:
    def __init__(self):
        # Create a deck

        self.deck = []

        faceValues = ["A", "K", "Q", "J"]

        for i in range(4):
            for card in range(2,11):
                self.deck.append(str(card))
            for card in faceValues:
                self.deck.append(card)

        shuffle(self.deck)

    def getHalves(self):
        return self.deck[:26], self.deck[26:]

=======
from random import shuffle

class Deck:
    def __init__(self):
        # Create a deck

        self.deck = []

        faceValues = ["A", "K", "Q", "J"]

        for i in range(4):
            for card in range(2,11):
                self.deck.append(str(card))
            for card in faceValues:
                self.deck.append(card)

        shuffle(self.deck)

    def getHalves(self):
        return self.deck[:26], self.deck[26:]

>>>>>>> a8b2937820a192227135ebe91399e7f31b4c7084
