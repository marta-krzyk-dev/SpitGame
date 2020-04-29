def tryConvertToInt(value):

    if isinstance(value, str):
        value = value.strip()

    try:
        return int(value)  # If conversion is a success, return the integer
    except ValueError:
        return False