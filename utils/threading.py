from threading import Thread

#Not sure I wrote this code. 
#I suppose I didn't, but found it as tutorials.
#If this is yours, please, tell me.

def threadize(function):
    '''
    Make a function run asyncronously in a parallel thread.
    '''
    def inner(*args, **kwargs):
        class ThreadDeco(Thread):
            def run(self):
                function(*args, **kwargs)
        t = ThreadDeco()
        t.start()
        t.__name__ = function.__name__
        return t
    return inner

def daemonize(function):
    '''
    Make a function run asyncronously in a parallel thread
    as a hell's Daemon.
    '''
    def inner(*args, **kwargs):
        class DaemonDeco(Thread):
            def run(self):
                function(*args, **kwargs)
        t = DaemonDeco()
        t.setDaemon(True)
        t.start()
        t.__name__ = function.__name__
        return t
    return inner
    
#For compatibilities with other modules and stuff of my own:
make_thread = threadize
make_daemon = daemonize
