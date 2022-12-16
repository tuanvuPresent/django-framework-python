from apps.common.enum import EnumMeta


class UserType(EnumMeta):
    STAFF = (0, 'user')
    ADMIN = (1, 'admin')
    CEO = (2, 'ceo')
    LEADER = (3, 'leader')


class GenderType(EnumMeta):
    MALE = (0, 'Male')
    FEMALE = (1, 'Female')
