from dataclasses import dataclass
from enum import Enum, auto

from states.idle import idle
from states.confirm_state_popup import confirm_popup
from states.select_boost import select_boost
from states.start_from_lobby import start_from_lobby
from states.start_from_boost import start_from_boost
from states.in_game import in_game
from states.end_match_ok import end_match_ok
from states.open_box import open_box

class state_enum(Enum):
    Idle = auto()
    ConfirmPopup = auto()
    StartFromLobby = auto()
    SelectBoost = auto()
    StartFromBoost = auto()
    InGame = auto()
    MatchEnd = auto()
    OpenBox = auto()


handler = {
    state_enum.Idle: idle,
    state_enum.ConfirmPopup: confirm_popup,
    state_enum.StartFromLobby: start_from_lobby,
    state_enum.SelectBoost: select_boost,
    state_enum.StartFromBoost: start_from_boost,
    state_enum.InGame: in_game,
    state_enum.MatchEnd: end_match_ok,
    state_enum.OpenBox: open_box,
}


@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, state):
        self.state = state
        handler[state](self, state_enum)
