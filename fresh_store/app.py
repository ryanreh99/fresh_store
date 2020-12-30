from .exceptions import (
    KeyAlreadyExists,
)

from . import utils

"""
THE DATA STORE IS A JSON FILE
WHERE KEY IS MAPPED TO AN ARRAY
WHOSE 1ST ELEMENT IS A JSON DATA
AND 2ND ELEMENT IS THE EXPIRY TIME. (OR -1)
"""


class FreshStore:
    def __init__(self, file_path: str = None):
        self.file_path = utils.initialize_date_store_file(file_path)

    def _get_data_store_file(self):
        return self.file_path

    def _get_data_store(self, is_empty: bool = False) -> dict:
        data_store_file: str = self._get_data_store_file()
        return utils.get_data_store(data_store_file, is_empty)

    @staticmethod
    def _validate_key(key: str) -> None:
        return utils.validate_key(key)

    @staticmethod
    def _validate_value(value_file: str) -> int:
        return utils.validate_value(value_file)

    @staticmethod
    def _validate_date(expiry: str, key: str) -> None:
        return utils.validate_date(expiry, key)

    def _validate_data_store(self, val_size: int) -> bool:
        data_store: str = self._get_data_store_file()
        return utils.validate_data_store(data_store, val_size)

    def _validation(self, *args):
        """
        Validate key, value(if required) and data store
        :param args: 1st param - key to be created / read / deleted ...
                     2nd param - [OPTIONAL] file name / value to be validated before storing.
        :return: 1st param - the path of the file to be stored.
                 2nd param - the data store object.
        """
        key = args[0]
        self._validate_key(key)
        val_size = 0
        value_file: str = ""

        if len(args) == 2:
            value_file = args[1]
            val_size: int = self._validate_value(value_file)

        is_empty: bool = self._validate_data_store(val_size)
        data_store: dict = self._get_data_store(is_empty)
        return value_file, data_store

    def _rewrite_data_store(self, new_data_store: dict) -> None:
        data_store_file: str = self._get_data_store_file()
        return utils.rewrite_data_store(data_store_file, new_data_store)

    @staticmethod
    def _load_json_file(value_file):
        return utils.load_json_file(value_file)

    def create(self, key: str, val_file: str = "example_1.json", ttl: int = -1) -> None:
        """
        Creates an entry.
        :param ttl: Time in seconds
        :param key: key to be stored
        :param val_file: the file containing the value
        :return: None
        """
        value_file, data_store = self._validation(key, val_file)

        json_file: dict = self._load_json_file(value_file)

        # Creating new data store obj
        if key in data_store:
            # FUNCTIONAL REQUIREMENTS - POINT 3
            raise KeyAlreadyExists(key)

        expiry = utils.get_expiry_date(ttl)
        new_value = [json_file, expiry]
        data_store[key] = new_value

        self._rewrite_data_store(data_store)
        print("ENTRY CREATED!")

    def read(self, key: str) -> str:
        """
        Reads an entry if it exists.
        :param key: the key to search.
        :return: the entry if found else ""
        """
        _, data_store = self._validation(key)

        if key not in data_store:
            print("NOT FOUND")
            return ""

        expiry = data_store.get(key)[1]
        self._validate_date(expiry, key)

        # FUNCTIONAL REQUIREMENTS - POINT 4
        ret = data_store.get(key)[0]
        print("DATA RETURNED!")
        return ret

    def delete(self, key: str) -> str:
        """
        deletes an entry if present
        :param key: the key to search.
        :return: the now deleted entry if found else ""
        """
        _, data_store = self._validation(key)

        if key not in data_store:
            print("NOT FOUND")
            return ""

        expiry = data_store.get(key)[1]
        self._validate_date(expiry, key)

        ret = data_store.get(key)[0]
        data_store.pop(key, None)
        self._rewrite_data_store(data_store)

        # FUNCTIONAL REQUIREMENTS - POINT 5
        print("DATA DELETED!")
        return ret
