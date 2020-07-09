def num_padding(value: str) -> str:
    """
    Applies simple 0-prefix padding to date parts like month/day.
    :param value: The value to be padded.  Assumed to be a valid integer
    :return: The padded string
    """
    try:
        num = int(value)
        if num < 10:
            return f"0{num}"
        else:
            return str(num)
    except ValueError:
        # The validator will catch these -- this allows optional fields that are empty strings
        # to use this converter function and not bomb out.
        return value
