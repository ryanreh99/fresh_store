import os
import json

from .exceptions import (
    KeyAlreadyExists,
)
from .data import (
    DATA_STORE_FILE_NAME,
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
        if file_path is None:
            # FUNCTIONAL REQUIREMENTS - POINT 1
            # If File Path is not provided, then set it as the
            # current directory from where the script was called.
            file_path = os.path.join(os.getcwd(), DATA_STORE_FILE_NAME)
        self.file_path = file_path

        if not os.path.exists(self._get_data_store_file()):
            # Create data store if does not exist
            with open(self._get_data_store_file(), 'w'):
                pass

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
            file_name = args[1]
            value_file = os.path.join(self.file_path, file_name)
            val_size: int = self._validate_value(value_file)

        is_empty: bool = self._validate_data_store(val_size)
        data_store: dict = self._get_data_store(is_empty)
        return value_file, data_store

    def _rewrite_data_store(self, new_data_store: dict) -> None:
        # Serialize data to be able to store more files.
        # NON-FUNCTIONAL REQUIREMENTS - POINT 4
        json_data_store: str = json.dumps(new_data_store, default=str)

        with open(self._get_data_store_file(), "w") as f:
            # Override entire file
            f.write(json_data_store)

    def create(self, key: str, file_name: str = "example_1.json", ttl: int = -1) -> None:
        """
        Creates an entry.
        :param ttl: Time in seconds
        :param key: key to be stored
        :param file_name: the file containing the value
        :return: None
        """
        value_file, data_store = self._validation(key, file_name)

        # Loading new data
        with open(value_file, "r") as f:
            # file closes after the execution of this block is completed.
            file_data = f.read()

        json_file: dict = json.loads(file_data)

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
