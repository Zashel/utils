import os
from .exceptions import PathError

#Not sure I wrote this code. 
#I suppose I didn't, but found it as tutorials.
#If this is yours, please, tell me.

def search_win_drive(path):
    '''
    Searches for a drive in a windows machine given a path to 
    look for from root.
    Returns the full path with the given path or raises
    PathError if not found.
    '''
    drives = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for drive in drives:
        full_path = r"{}:\{}".format(drive, path)
        if os.path.exists(full_path):
            return full_path
    else:
        raise FileNotFoundError

#For compatibilities with other modules and stuff of my own:
buscar_unidad = search_win_drive
