import enum
from abc import ABC, abstractmethod

from ai import AI, AIList
from fighter_actions import ActionList


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


class Fighter(ABC):
    ai: AI
    current_health: int
    opponent_attack_history: list
    opponent_block_history: list
    prepared_actions: list
    possible_actions: list
    current_attack: int = 0
    current_block: int = 0
    fighter_name: str

    def __init__(self):
        self.opponent_attack_history = []
        self.opponent_block_history = []
        self.possible_actions = []
        self.prepared_actions = []
        self.current_attack = 0
        self.current_block = 0
        self.fighter_name = 'No name'

    @abstractmethod
    def __str__(self):
        return f'Fighter {self.fighter_name}'

    @abstractmethod
    def prepare_actions(self, *args, **kwargs) -> int or None:
        ...


class Boxer(Fighter):

    def __init__(self, ai_class: AI, current_health: int, name: str = None):
        super().__init__()
        self.ai = ai_class
        self.current_health = current_health
        self.possible_actions = [ActionList.attack, ActionList.block]
        self.fighter_name = name

    def __str__(self):
        return f'Boxer "{self.fighter_name}"'

    def prepare_actions(self) -> list:
        self.prepared_actions = [act() for act in self.possible_actions]

        return self.prepared_actions

    def _make_action(self, action: Actions) -> BodyParts:
        if self.type == PlayerType.ROBOT:
            result = self._reflect(action)

        else:
            result = Game.input_body_part(action)

        return result

    def _reflect(self, action: Actions) -> BodyParts:
        predict = None
        opponent_history = self.opponent_block_history \
            if action == Actions.attack else self.opponent_attack_history

        predict = self.ai.make_choice(opponent_history)

        predict = predict if predict is not None \
            else Game.get_random_body_part()
        result = predict if action == Actions.block \
            else Game.get_random_body_part(exclude=predict)

        return result