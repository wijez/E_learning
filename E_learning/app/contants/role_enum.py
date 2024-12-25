from enum import Enum


class RoleEnum(Enum):
    SUPER_USER= "SUPER_USER"
    USER = "USER"
    ADMIN = "ADMIN"
    LECTURER = "LECTURER"

    @classmethod
    def choice(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_