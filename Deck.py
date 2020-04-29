from random import shuffle


class Deck:
    def __init__(self):
        self.deck = []
        faceValues = ["A", "K", "Q", "J"]

        for i in range(4):
            for card in range(2, 11):
                self.deck.append(str(card))
            for card in faceValues:
                self.deck.append(card)

        shuffle(self.deck)

    def getHalves(self):
        return self.deck[:26], self.deck[26:]
