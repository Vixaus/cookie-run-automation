from dataclasses import dataclass
from enum import Enum, auto

from states.confirm_state_popup import confirm_popup
from states.select_boost import select_boost
from states.start_from_lobby import start_from_lobby
from states.start_from_boost import start_from_boost

class state_enum(Enum):
    Idle = auto()
    StartFromLobby = auto()
    ConfirmPopup = auto()
    SelectBoost = auto()
    StartFromBoost = auto()


handler = {
    state_enum.Idle: lambda: None,
    state_enum.StartFromLobby: start_from_lobby,
    state_enum.ConfirmPopup: confirm_popup,
    state_enum.SelectBoost: select_boost,
    state_enum.StartFromBoost: start_from_boost,
}


@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, state):
        self.state = state

        if not state == state_enum.Idle:
            handler[state](self, state_enum)

        return
