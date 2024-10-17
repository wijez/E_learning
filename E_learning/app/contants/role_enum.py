from enum import Enum


class RoleEnum(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

    @classmethod
    def choice(cls):
        return [(choice.name, choice.value) for choice in cls]
