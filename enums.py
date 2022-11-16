import enum


@enum.unique
class PlayerType(enum.IntEnum):
    ROBOT = 0
    HUMANOID = 1


@enum.unique
class BodyParts(enum.IntEnum):
    HEAD = 1
    BODY = 2


@enum.unique
class Actions(enum.IntEnum):
    attack = -1
    block = 1


class TypeAI(enum.IntEnum):
    RND = 0
    MOST_COMMON = 1
