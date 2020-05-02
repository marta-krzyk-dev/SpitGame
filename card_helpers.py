from Project4_Split.Deck import Deck
from Project4_Split.helpers import tryConvertToInt


def IsValidPair(card1, card2):
    card1 = ConvertCardToNumericValue(card1)
    card2 = ConvertCardToNumericValue(card2)
    diff = abs(card1 - card2)

    return diff < 2 or diff == 12  # Cards have 0, 1 or 12 value difference. (one card is 2, the other is A)


def ThereAreValidPairs(set1, set2):
    # Check if parameters are iterables
    try:
        iter(set1)
        iter(set2)
    except TypeError:
        return False

    set1 = set(set1)  # Remove duplicates if lists were provided
    set2 = set(set2)

    for card1 in set1:
        for card2 in set2:
            if IsValidPair(card1, card2):

                return True  # There is at least 1 valid pair

    return False


def ConvertCardToNumericValue(card):
    if not (isinstance(card, str) or isinstance(card, int)):
        raise TypeError

    card_as_number = tryConvertToInt(card)

    if not card_as_number:
        if card in Deck.faceValues:
            return Deck.faceValues[card]
        else:
            raise ValueError
    else:
        return card_as_number
