from functools import wraps
from os.path import exists, split
import pprint


class Log:
    screen = True


def log(function, log=Log):
    @wraps(function)
    def inner(*args, **kwargs):
        if log.screen is True:
            print("Call of function {}:\n\targs:\t{}\n\tkwargs:\t{}\n".format(function.__name__,
                                                                           pprint.pformat(args),
                                                                           pprint.pformat(kwargs)))
        final = function(*args, **kwargs)
        if log.screen is True:
            print("Return of function {}:\n\t{}\n".format(function.__name__,
                                                        pprint.pformat(final)))
        return final
    return inner