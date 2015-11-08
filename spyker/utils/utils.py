import os


def is_valid_path(path):
    try:
        open(path, 'w')
        print "good"
        os.unlink(path)
        return True
    except (IOError, OSError):
        print "bad"
        return False


def is_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
