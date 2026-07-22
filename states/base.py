import time

from dataclasses import dataclass
from enum import Enum, auto

from states.idle import idle
from states.confirm_popup import confirm_popup
from states.buy_random_boost import buy_random_boost
from states.start_from_lobby import start_from_lobby
from states.start_from_boost import start_from_boost
from states.in_game import in_game
from states.end_match import end_match_ok
from states.open_box import open_box
from states.close_x_popup import close_x_popup
from states.get_relic import get_relic
from states.cookie_relay import cookie_relay
from states.buy_boost import buy_boost

class state_enum(Enum):
    Idle = auto()
    CloseXPopup = auto()
    ConfirmPopup = auto()
    GetRelic = auto()
    StartFromLobby = auto()
    BuyBoost = auto()
    RandomBoost = auto()
    StartFromBoost = auto()
    InGame = auto()
    MatchEnd = auto()
    OpenBox = auto()
    CookieRelay = auto()


handler = {
    state_enum.Idle: idle,
    state_enum.CloseXPopup: close_x_popup,
    state_enum.ConfirmPopup: confirm_popup,
    state_enum.GetRelic: get_relic,
    state_enum.StartFromLobby: start_from_lobby,
    state_enum.BuyBoost: buy_boost,
    state_enum.RandomBoost: buy_random_boost,
    state_enum.StartFromBoost: start_from_boost,
    state_enum.InGame: in_game,
    state_enum.MatchEnd: end_match_ok,
    state_enum.OpenBox: open_box,
    state_enum.CookieRelay: cookie_relay,
}


@dataclass
class bot_state:
    state: state_enum = state_enum.Idle

    def update(self, state):
        print(state)
        self.state = state

    def run(self):

        while True:
            handler[self.state](self, state_enum)
            time.sleep(0.5)
