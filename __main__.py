import random

from enums import PlayerType, BodyParts, Actions, TypeAI
from collections import Counter


class Game:
    MAX_HEALTH = 3
    MAX_MOVES = MAX_HEALTH * 2

    def __init__(self, boxer1, boxer2):
        self.boxer1 = boxer1
        self.boxer2 = boxer2
        self.current_step = 0

    class Boxer:

        def __init__(self, player_type: PlayerType = PlayerType.ROBOT,
                     type_ai: TypeAI = TypeAI.MOST_COMMON):
            self.type: PlayerType = player_type
            self.type_ai: TypeAI = type_ai
            self.current_health: int = Game.MAX_HEALTH
            self.opponent_attack_history: list[int] = []
            self.opponent_block_history: list[int] = []
            self.current_attack: int = 0
            self.current_block: int = 0

        def attack(self) -> BodyParts:
            attack = self._make_action(Actions.attack)
            self.current_attack = attack

            return attack

        def block(self) -> BodyParts:
            block = self._make_action(Actions.block)
            self.current_block = block

            return block

        def prepare_actions(self) -> None:
            self.attack()
            self.block()

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

            if self.type_ai == TypeAI.MOST_COMMON:
                predict = Game.get_most_common_body_parts(opponent_history)

            predict = predict if predict is not None \
                else Game.get_random_body_part()
            result = predict if action == Actions.block \
                else Game.get_random_body_part(exclude=predict)

            return result

    @staticmethod
    def get_most_common_body_parts(data: list[int]) -> BodyParts or None:
        most_common = Counter(data).most_common(1)
        result = None if len(most_common) == 0 else most_common[0][0]

        return result

    @staticmethod
    def get_random_body_part(exclude: BodyParts = None) -> BodyParts:
        if exclude:
            result = exclude

            while result == exclude:
                result = random.choice(list(BodyParts))

        else:
            result = random.choice(list(BodyParts))

        return result

    @staticmethod
    def _get_health_as_str(health: int) -> str:
        symbol_on = '█'
        symbol_off = '░'
        health = (symbol_on * health) + \
                 (symbol_off * (Game.MAX_HEALTH - health))

        return health

    @staticmethod
    def input_body_part(action: Actions) -> BodyParts or None:
        counter = 0
        max_counter = 3
        input_body_part_value = 0

        while counter < max_counter \
                and input_body_part_value not in list(BodyParts):
            counter += 1
            print(f'Enter {action.name} (head - {BodyParts.HEAD.value}, '
                  f'body - {BodyParts.BODY.value}):')
            try:
                input_body_part_value = int(input())

            except ValueError:
                ...

        result = None if input_body_part_value not in list(BodyParts) \
            else BodyParts(input_body_part_value)

        if result is None:
            Game.print_game_over()
            exit(result)

        return result

    def print_health_stripes(self) -> None:
        fighter1 = self.boxer1
        fighter2 = self.boxer2
        player1_health_str = self._get_health_as_str(fighter1.current_health)
        player2_health_str = self._get_health_as_str(fighter2.current_health)
        print(f'Player1: [{player1_health_str}] '
              f'Player2: [{player2_health_str}]')

    @staticmethod
    def print_introduction() -> None:
        print('Let\'s get ready to rumble!')
        print(f'---------- BOX!!! ----------')

    def print_intermediate_fight_result(self) -> None:
        move = self.current_step
        print(f'***** STEP {move} *****')
        self.print_health_stripes()

    def print_fight_result(self) -> None:
        fighter1 = self.boxer1
        fighter2 = self.boxer2
        print(
            f'Player1 attack: {BodyParts(fighter1.current_attack).name},'
            f' Player2 block: {BodyParts(fighter2.current_block).name}\n'
            f'Player2 attack: {BodyParts(fighter2.current_attack).name},'
            f' Player1 block: {BodyParts(fighter1.current_block).name}'
        )

    def print_fight_result_final(self) -> None:
        fighter1 = self.boxer1
        fighter2 = self.boxer2
        print(f'***** RESULT *****')
        self.print_health_stripes()
        if fighter1.current_health == fighter2.current_health:
            print('Draw!')
        elif fighter1.current_health == 0:
            print('Player1 lose! Player2 win!')
        else:
            print('Player1 win! Player2 lose!')

    @staticmethod
    def print_game_over() -> None:
        print('Game over!')

    def summarize(self) -> None:
        fighter1 = self.boxer1
        fighter2 = self.boxer2

        fighter1_block_performance = \
            fighter1.current_block == fighter2.current_attack
        fighter1_attack_performance = \
            fighter1.current_attack != fighter2.current_block

        fighter1.current_health += -1 if not fighter1_block_performance else 0
        fighter1.opponent_attack_history.append(fighter2.current_attack)
        fighter1.opponent_block_history.append(fighter2.current_block)

        fighter2.current_health += -1 if fighter1_attack_performance else 0
        fighter2.opponent_attack_history.append(fighter1.current_attack)
        fighter2.opponent_block_history.append(fighter1.current_block)

    def start(self) -> None:
        self.current_step = 0
        Game.print_introduction()

        while self.boxer1.current_health > 0 \
                and self.boxer2.current_health > 0 \
                and self.current_step < self.MAX_MOVES:
            self.current_step += 1
            self.print_intermediate_fight_result()
            self.boxer1.prepare_actions()
            self.boxer2.prepare_actions()
            self.print_fight_result()
            self.summarize()

        self.print_fight_result_final()
        self.print_game_over()


if __name__ == '__main__':
    player1 = Game.Boxer(type_ai=TypeAI.RND)
    player2 = Game.Boxer(type_ai=TypeAI.MOST_COMMON)
    game = Game(player1, player2)
    game.start()
