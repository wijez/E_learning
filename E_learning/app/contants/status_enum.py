from enum import Enum


class StatusEnum(Enum):
    IN_PROCESS = "IN PROCESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    @classmethod
    def choice(cls):
        return [(choice.name, choice.value) for choice in cls]

class ChoicesEnum(Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"

    @classmethod
    def choice(cls):
        return [(choice.name, choice.value) for choice in cls]