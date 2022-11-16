import enum
import random
from abc import ABC, abstractmethod
from collections import Counter


class AI(ABC):
    @staticmethod
    @abstractmethod
    def make_choice(*args, **kwargs) -> int or None:
        ...


class AIMostCommon(AI):
    @staticmethod
    def make_choice(data: list[int]):
        most_common = Counter(data).most_common(1)
        result = None if len(most_common) == 0 else most_common[0][0]

        return result


class AIRandom(AI):
    @staticmethod
    def make_choice(data: list[int], exclude: int or None = None):
        if exclude:
            result = exclude

            while result == exclude:
                result = random.choice(data)

        else:
            result = random.choice(data)

        return result


@enum.unique
class AIList(enum.Enum):
    RND = AIRandom()
    MOST_COMMON = AIMostCommon()
