from threading import Thread
from multiprocessing import Pipe
from functools import wraps


def threadize(function):
    '''
    Make a function run asynchronously in a parallel thread.
    It returns the thread to join.

    :param function: Function to run in a different thread
    :return: Thread to be joined

    '''
    @wraps(function)
    def inner(*args, **kwargs):
        class ThreadDeco(Thread):
            def run(self):
                function(*args, **kwargs)
        t = ThreadDeco()
        t.start()
        t.__class__ = Thread
        t.__name__ = function.__name__
        return t
    return inner


def daemonize(function):
    '''
    Make a function run asynchronously in a parallel thread
    as a hell's Daemon.
    It returns the thread.

    :param function: Function to run in a different thread
    :return: Thread to be joined

    '''
    @wraps(function)
    def inner(*args, **kwargs):
        class DaemonDeco(Thread):
            def run(self):
                function(*args, **kwargs)
        t = DaemonDeco()
        t.setDaemon(True)
        t.start()
        t.__class__ = Thread
        t.__name__ = function.__name__
        return t
    return inner


def asynchronic(function):
    """
    Returns a pipe from wich the returning object may be taken.
    It is not a daemon.

    :param function: Function to run in a different thread
    :return: A pipe from which the returning object can be taken

    """
    @threadize
    def in_thread(pipeout, *args, **kwargs):
        data = function(*args, **kwargs)
        pipeout.send(data)
    @wraps(function)
    def inner(*args, **kwargs):
        pipein, pipeout = Pipe()
        in_thread(pipeout, *args, **kwargs)
        pipein.__name__ = function.__name__
        return pipein
    return inner


#For compatibilities with other modules and stuff of my own:
make_thread = threadize
make_daemon = daemonize
