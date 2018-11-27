import json
import os
import re


def load_json(filepath: str, make = True):
    """Opens a JSON file in the given directory returns the dict loaded.
    If no file is present and make is False, returns None.
    Else, it creates the file and returns an empty JSON."""
    if not os.path.isfile(filepath):
        if make:
            json.dump({}, open(filepath, 'w'), indent = 2)
        else:
            return None
    else:
        with open(filepath, 'r') as _file:
            return json.load(_file)


def dump_json(filepath: str, _dict, make = True):
    """Opens a JSON file in the given directory dumps the dict given.
    If no file is present and make is False, raises FileNotFoundError.
    Else, it creates the file and dumps into it."""
    if not os.path.isfile(filepath):
        if make:
            json.dump(_dict, open(filepath, 'w'), indent = 2)
    else:
        with open(filepath, 'w') as _file:
            json.dump(_dict, _file, indent = 2)


def reg_searcher(string: str, regex, *, clean = True):
    """Converts a normal string into a regex string. Intended for converting strings from json files."""

    if clean:
        string = re.sub(r'[^a-z\d\s]+', '', string.lower())

    if type(regex) == list:
        for reg in regex:
            if bool(re.search(reg, string)):
                return True
        return False

    elif type(regex) == str:
        return bool(re.search(regex, string))

    else:
        raise TypeError


def merge(a, b):
    """Merges b into a"""
    if isinstance(a, dict) and isinstance(b, dict):
        for key in b:
            if key not in a:
                a[key] = b[key]
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key])
            else:
                a[key] = b[key]
    else:
        raise TypeError
