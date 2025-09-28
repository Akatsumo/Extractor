import string

a_to_zList = {
    f"appxSection_{letter}": {"name": letter}
    for letter in string.ascii_uppercase
}
