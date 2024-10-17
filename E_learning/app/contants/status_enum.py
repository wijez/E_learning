from enum import Enum


class StatusEnum(Enum):
    IN_PROCESS = "IN PROCESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    @classmethod
    def choice(cls):
        return [(choice.name, choice.value) for choice in cls]
