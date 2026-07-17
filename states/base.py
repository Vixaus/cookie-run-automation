from dataclasses import dataclass
from enum import Enum, auto

from states.select_boost import select_boost
from states.start_game import start_game


class state_enum(Enum):
    Idle = auto()
    StartGame = auto()
    SelectBoost = auto()


handler = {
    state_enum.Idle: None,
    state_enum.StartGame: start_game,
    state_enum.SelectBoost: select_boost,
}


@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, state):
        self.state = state

        handler[state](self, state_enum)

        return
