import os
import json
import datetime

from .exceptions import (
    KeyCapacityExceededError,
    ValueCapacityExceededError,
    KeyExpired,
)
from .data import (
    MAX_KEY_CAPACITY,
    MAX_VALUE_SIZE,
    MAX_DATA_STORE_SIZE,
)


def validate_key(key: str) -> None:
    """
    Validates key to be created or accessed.
    :param key: the key to be checked
    :return: None
    """
    if len(key) > MAX_KEY_CAPACITY:
        # FUNCTIONAL REQUIREMENTS - POINT 2
        raise KeyCapacityExceededError(key)


def validate_value(value_file: str) -> int:
    """
    Validates value to be stored.
    :param value_file:
    :return: The file size to validate the data store file also.
    """
    file_size: int = os.stat(value_file).st_size
    if file_size > MAX_VALUE_SIZE:
        # FUNCTIONAL REQUIREMENTS - POINT 2
        raise ValueCapacityExceededError(is_internal=False, max_size=MAX_VALUE_SIZE)

    return file_size


def validate_data_store(data_store: str, val_size: int) -> bool:
    """
    Validates the data store file.
    :param data_store: the data store file.
    :param val_size: size of the file to be added,
                     so that we can calculate the new size.
    :return: Whether the data store is empty or not
    """
    data_store_size: int = os.stat(data_store).st_size
    if data_store_size + val_size > MAX_DATA_STORE_SIZE:
        # # NON-FUNCTIONAL REQUIREMENTS - POINT 1
        raise ValueCapacityExceededError(is_internal=True, max_size=MAX_VALUE_SIZE)

    return data_store_size == 0


def validate_date(expiry: str, key: str) -> None:
    current_time = datetime.datetime.now()
    expiry_time = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")

    if current_time > expiry_time:
        raise (KeyExpired("key"))


def get_expiry_date(ttl: int):
    # FUNCTIONAL REQUIREMENTS - POINT 6
    expiry = -1
    if ttl is not -1:
        current_time = datetime.datetime.now()
        expiry = current_time + datetime.timedelta(seconds=ttl)

    return expiry


def get_data_store(data_store_file: str, is_empty: bool = False) -> dict:
    """
    To get the data store object and check for empty file case.
    :param data_store_file: the data store file.
    :param is_empty: for the check
    :return: the data store object
    """
    if not is_empty:
        with open(data_store_file, "r") as f:
            data_store: str = f.read()

        json_data_store_file: dict = json.loads(data_store)
    else:
        # Loading empty file raises json.decoder.JSONDecodeError error.
        json_data_store_file = {}

    return json_data_store_file