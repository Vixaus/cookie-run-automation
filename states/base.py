from dataclasses import dataclass
from enum import Enum, auto
from states.start_game import start_game
from states.select_boost import select_boost


class state_enum(Enum):
    Idle = auto()
    StartGame = auto()
    SelectBoost = auto()

handler = [
    {
        "state": state_enum.StartGame,
        "action": start_game
    },
    {
        "state": state_enum.SelectBoost,
        "action": select_boost
    }
]

@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, state):
        self.state = state

        for h in handler:
            if h["state"] == state:
                h["action"](self, state_enum)
                break
        return
