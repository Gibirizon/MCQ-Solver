from enum import Enum, auto


class ResponseStatus(Enum):
    SUCCESS = auto()
    MISSING_ERROR_FIELD = auto()
    MISSING_RESULT_FIELD = auto()
    ERROR_REPORTED = auto()
