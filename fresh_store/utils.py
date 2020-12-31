import os
import json
import datetime

from .data import (
    get_MAX_KEY_CAPACITY,
    get_MAX_VALUE_SIZE,
    get_MAX_DATA_STORE_SIZE,
    get_DATA_STORE_FILE_NAME,
)
from .exceptions import (
    KeyCapacityExceededError,
    ValueCapacityExceededError,
    KeyExpired,
)


def initialize_date_store_file(file_path: str = None) -> str:
    """
    initializes file path and creates file if does not exist
    :param file_path: [ OPTIONAL ] entire path of data store file.
    :return: returns entire path of data store file.
    """
    if file_path is None:
        # FUNCTIONAL REQUIREMENTS - POINT 1
        # If File Path is not provided, then set it as the
        # current directory from where the script was called.
        file_path = os.path.join(os.getcwd(), get_DATA_STORE_FILE_NAME())

    if not os.path.exists(file_path):
        # Create data store if does not exist
        with open(file_path, 'w'):
            pass

    return file_path


def overwrite_data_store(data_store_file: str, new_data_store: dict) -> None:
    """
    Over write the data store file
    :param data_store_file: the data store file to over write.
    :param new_data_store: the new json object.
    :return: None
    """
    # Serialize data to be able to store more files.
    # NON-FUNCTIONAL REQUIREMENTS - POINT 4
    json_data_store: str = json.dumps(new_data_store, default=str)

    with open(data_store_file, "w") as f:
        f.write(json_data_store)


def load_json_file(file_path: str) -> dict:
    """
    load a json file.
    :param file_path: entire file path
    :return: the json object
    """
    with open(file_path, "r") as f:
        # file closes after the execution of this block is completed.
        file_data = f.read()

    if len(file_data) == 0:
        # Loading empty file raises json.decoder.JSONDecodeError error.
        return {}

    return json.loads(file_data)


def validate_key(key: str) -> None:
    """
    Validates key to be created or accessed.
    :param key: the key to be checked
    :return: None
    """
    if len(key) > get_MAX_KEY_CAPACITY():
        # FUNCTIONAL REQUIREMENTS - POINT 2
        raise KeyCapacityExceededError(key)


def validate_value(value_file: str) -> int:
    """
    Validates value to be stored.
    :param value_file:
    :return: The file size to validate the data store file also.
    """
    file_size: int = os.stat(value_file).st_size
    if file_size > get_MAX_VALUE_SIZE():
        # FUNCTIONAL REQUIREMENTS - POINT 2
        raise ValueCapacityExceededError(is_internal=False, max_size=get_MAX_VALUE_SIZE())

    return file_size


def validate_data_store(data_store_file: str, val_size: int) -> bool:
    """
    Validates the data store file.
    :param data_store_file: the data store file.
    :param val_size: size of the file to be added,
                     so that we can calculate the new size.
    :return: Whether the data store is empty or not
    """
    data_store_size: int = os.stat(data_store_file).st_size
    if data_store_size + val_size > get_MAX_DATA_STORE_SIZE():
        # NON-FUNCTIONAL REQUIREMENTS - POINT 1
        raise ValueCapacityExceededError(is_internal=True, max_size=get_MAX_DATA_STORE_SIZE())

    return data_store_size == 0


def validate_date(expiry: str, key: str) -> None:
    """
    Validates whether the data can be accessed or not
    :param expiry: the expire date or -1 (for infinite).
    :param key: the key to access the data.
    :return: None
    """
    if type(expiry) == int:
        return
    current_time = datetime.datetime.now()
    expiry_time = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")

    if current_time > expiry_time:
        raise KeyExpired(key)


def get_expiry_date(ttl: int):
    """
    Calculate and return the expire date or -1.
    :param ttl: Time To Live property
    :return: A datetime object
    """
    # FUNCTIONAL REQUIREMENTS - POINT 6
    expiry = -1
    if ttl is not -1:
        current_time = datetime.datetime.now()
        expiry = current_time + datetime.timedelta(seconds=ttl)

    return expiry


def get_data_store(data_store_file: str) -> dict:
    """
    To get the data store object and check for empty file case.
    :param data_store_file: the data store file.
    :return: the data store object
    """
    json_data_store_file: dict = load_json_file(data_store_file)

    return json_data_store_file
