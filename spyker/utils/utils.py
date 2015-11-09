import os


def is_valid_path(path):
    try:
        open(path, 'w')
        os.unlink(path)
        return True
    except (IOError, OSError):
        return False


def is_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
