<<<<<<< HEAD
def tryConvertToInt(value):

    if isinstance(value, str):
        value = value.strip()

    try:
        return int(value)  # If conversion is a success, return the integer
    except Exception:
        return False


def getFirst(iterable, default= ' '):
    return iterable[0] if isinstance(iterable, list) and len(iterable) > 0 else default

def getFirstElements(*elements):
    iterable = list(elements)
    if len(iterable) == 0:
        return []

    result = []

    for element in iterable:
        if len(element) > 0:
            if element[0] != 0 and element[0] != " ":
                result.append(element[0])

    return result
=======
def tryConvertToInt(value):

    if isinstance(value, str):
        value = value.strip()

    try:
        return int(value)  # If conversion is a success, return the integer
    except Exception:
        return False


def getFirst(iterable, default= ' '):
    return iterable[0] if isinstance(iterable, list) and len(iterable) > 0 else default

def getFirstElements(*elements):
    iterable = list(elements)
    if len(iterable) == 0:
        return []

    result = []

    for element in iterable:
        if len(element) > 0:
            if element[0] != 0 and element[0] != " ":
                result.append(element[0])

    return result
>>>>>>> a8b2937820a192227135ebe91399e7f31b4c7084
