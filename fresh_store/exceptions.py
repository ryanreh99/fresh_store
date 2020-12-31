# FUNCTIONAL REQUIREMENTS - POINT 7

class KeyException(Exception):
    # The following few classes inherits this class.
    def __init__(self, info: str):
        self.key = info


class KeyCapacityExceededError(KeyException):
    def __str__(self):
        return f"Key: {self.key} exceeds the 32 characters capacity."


class KeyAlreadyExists(KeyException):
    def __str__(self):
        return f"Key: {self.key} already exists in the data store."


class KeyExpired(KeyException):
    def __str__(self):
        return f"Key: {self.key} expired."


class ValueCapacityExceededError(Exception):
    def __init__(self, **kwargs):
        # kwargs contains whether exception raised due to
        # internal data store or passed file to be stored.
        self.is_internal = kwargs.get("is_internal")
        self.max_size = kwargs.get("max_size")

    def __str__(self):
        name: str = "data store" if self.is_internal else "file"
        return f"{name} exceeds the {self.max_size}B size limit."
