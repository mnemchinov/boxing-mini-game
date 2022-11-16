import enum
from abc import ABC


@enum.unique
class BodyParts(enum.IntEnum):
    HEAD = 1
    BODY = 2


class Action(ABC):
    force: int
    aim: BodyParts

    def __init__(self, aim: BodyParts):
        self.aim = aim


class Attack(Action):
    force: int = 1
    aim: BodyParts


class Block(Action):
    force: int = 1
    aim: BodyParts


@enum.unique
class ActionList(enum.Enum):
    attack = Attack
    block = Block
