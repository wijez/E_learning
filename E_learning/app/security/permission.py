from E_learning.app.contants import RoleEnum
from E_learning.app.security.role_permission import IsRole


class IsAdmin(IsRole):
    def __init__(self):
        super().__init__([RoleEnum.ADMIN])


class IsLecturer(IsRole):
    def __init__(self):
        super().__init__([RoleEnum.LECTURER])


class IsUser(IsRole):
    def __init__(self):
        super().__init__([RoleEnum.USER])
