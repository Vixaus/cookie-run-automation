from dataclasses import dataclass
from enum import Enum

from .select_boost import select_boost
from .start_game import start_game


class state_enum(Enum):
    Idle = None
    StartGame = start_game()
    SelectBoost = select_boost()


@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, action):
        self.state = action
