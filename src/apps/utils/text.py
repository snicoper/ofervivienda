def ucfirst(string):
    """Obtener la primera letra en mayúsculas."""
    return '{}{}'.format(string[0].upper(), string[1:].lower())


def ucfirst_letter(string):
    """Primera letra de cada palabra en mayúsculas."""
    parts = string.split(' ')
    return ' '.join([ucfirst(l) for l in parts])
