import json
import logging
import os
from os.path import splitext, join
from random import randint


class DataIO:

    def __init__(self):
        self.logger = logging.getLogger("cueball")
        self.path = "data"

    def load_json(self, file: str):
        """
        Loads a json file.

        :param file: The json file to be loaded
        :return: dict of loaded json
        :rtype: dict
        """
        file = join(self.path, file) if self.path not in file else file

        if self.is_valid_json(file):
            try:
                with open(file, mode = 'r') as file:
                    return json.load(file)
            except json.decoder.JSONDecodeError:
                self.logger.error(f"Error while attempting to load {file}")
        else:
            raise FileNotFoundError

    def dump_json(self, file: str, data: dict):
        """
        Atomically saves a json file.

        :param file: The file where the data is to be dumped
        :param data: The dictionary to dump into a JSON file
        """
        file = join(self.path, file) if self.path not in file else file

        path, ext = splitext(file)
        tmp_file = f"{path}-{randint(1000, 9999)}.tmp"
        self._jdump(tmp_file, data)
        try:
            self.load_json(tmp_file)
            os.replace(tmp_file, file)
        except json.decoder.JSONDecodeError:
            self.logger.exception(f"Save to {file} aborted due to error. Data can be found in {tmp_file}.")

    def _jdump(self, file, data):
        file = join(self.path, file) if self.path not in file else file
        with open(file, 'w') as file:
            json.dump(data, file, indent = 2)
        return data

    def is_valid_json(self, file: str):
        """
        Checks if the file exists.

        :param file: The path of the file to be checked
        :return: If the file exists in the data folder
        :rtype: bool
        """
        file = join(self.path, file) if self.path not in file else file

        try:
            json.load(open(file, mode = 'r'))
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False

    def merge(self, a, b):
        """
        Merges b into a.

        :param a: dict being merged into (changing)
        :param b: dict being merged from (unchanging)
        :raises: TypeError
        """

        if isinstance(a, dict) and isinstance(b, dict):
            for key in b:
                if key not in a:
                    a[key] = b[key]
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key])
                else:
                    a[key] = b[key]
        else:
            raise TypeError


dataIO = DataIO()
