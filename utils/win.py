import datetime
import os
import win32clipboard as clipboard

SYLK_TEMPLATE = "ID;P\r\nP;PGeneral\r\n{}\r\nE"
FORMAT_RC_TEMPLATE = "F;P{format};{rc}{identifier}"
"""
format ->
    0: General
    1: Integer
    2: Decimal
    3: Euro
rc ->
    R: Row
    C: Column
identifier -> number identifing either column or row
"""
FORMAT_CELL_TEMPLATE = "F{coordinates};{p_format}F{format}{digits}{alignment}"
"""
coordinates -> use function coordinates
p_format -> As P{format} in FORMAT_RC_TEMPLATE, ending with ";"
format -> 
    C: currency
    E: exponent
    F: fixed
    G: general
    %: dollar
    *: graph
    %: percent
digits -> number of decimal digits
alingment ->
    C: center
    G: standard
    L: left
    R: right
    -: ignored
    X: fill
"""



def coordinates(column, row=None):
    final = str()
    if row is not None:
        final = ";".join([final, "Y"+str(row)])
    return ";".join([final, "X"+str(column)] )


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

def format_sylk(data):
    if isinstance(data, datetime.datetime):
        data = data.strftime("%d/%m/%Y %H:%M:%S")
    if isinstance(data, str):
        data = "\"" + data + "\""
    return str(data)

def copy(item):
    """
    Copies item to windows clipboard

    :param item: item to copy to
    :return: None
    """
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    if any([isinstance(item, typo) for typo in (list, tuple)]):
        headers = list()
        def set_headers(item):
            final = list()
            if headers == list():
                headers.extend(list(item.keys()))
                headers.sort()
                final.append("\t".join(headers))
            final.append("\t".join([str(item[head]) for head in headers]))
            return "\r\n".join(final)
        def set_sylk(item):
            final = list()
            row_index = 1
            for row in item:
                if any([isinstance(row, typo) for typo in (list, tuple)]):
                    for index, cell in enumerate(row):
                        final.append("C"+coordinates(index+1, row_index)+";K"+format_sylk(cell))
                    row_index += 1
                elif isinstance(row, dict):
                    h = list(row.keys())
                    h.sort()
                    if headers == list() or h != headers:
                        go_headers = True
                    else:
                        go_headers = False
                    set_headers(row)
                    if go_headers is True:
                        final.extend(["C"+coordinates(index+1, row_index)+";K"+format_sylk(head)
                                      for index, head in enumerate(headers)])
                        row_index += 1
                    final.extend(["C" + coordinates(index+1, row_index) + ";K" + format_sylk(row[head])
                                  for index, head in enumerate(headers)])
                    row_index += 1
                else:
                    final.append("C" + coordinates(1, row_index) + ";K" + format_sylk(row))
                    row_index += 1
            headers.clear()
            return "\r\n".join(final)
        clipboard.SetClipboardData(clipboard.CF_SYLK, bytearray(SYLK_TEMPLATE.format(set_sylk(item)), "utf-8"))
        clipboard.SetClipboardText("\r\n".join([any([isinstance(i, t) for t in (list, tuple)]) and
                                                "\t".join([str(a) for a in i]) or
                                                isinstance(i, dict) and set_headers(i) or
                                                str(i) for i in item]))
    else:
        clipboard.SetClipboardData(clipboard.CF_SYLK,
                                   bytearray(SYLK_TEMPLATE.format("C"+coordinates(1, 1)+";K"+format_sylk(item)), "utf-8"))
        clipboard.SetClipboardText(str(item))
    clipboard.CloseClipboard()


def paste():
    """
    Pastes item form windows clipboard

    :return: Contents from clipboard
    """
    clipboard.OpenClipboard()
    data = clipboard.GetClipboardData()
    clipboard.CloseClipboard()
    return data