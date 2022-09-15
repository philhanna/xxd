def parse_hex_digit(ch: str):
    """If "ch" is a hex digit, return the value.
    Otherwise, return -1."""
    c = ord(ch)
    value = -1
    if '0' <= ch <= '9':
        value = c - ord('0')
    elif 'a' <= ch <= 'f':
        value = c - ord('a') + 10
    elif 'A' <= ch <= 'F':
        value = c - ord('A') + 10
    return value
