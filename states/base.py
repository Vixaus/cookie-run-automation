import time
from dataclasses import dataclass
from enum import Enum, auto

from automation.bridge import emit
from states.idle import idle
from states.popup.close_x_popup import close_x_popup
from states.popup.confirm_popup import confirm_popup
from states.run.buy_boost import buy_boost
from states.run.buy_random_boost import buy_random_boost
from states.run.cookie_relay import cookie_relay
from states.run.end_match import end_match_ok
from states.run.get_relic import get_relic
from states.run.in_game import in_game
from states.run.open_box import open_box
from states.run.send_lives import send_lives
from states.run.start_from_boost import start_from_boost
from states.run.start_from_lobby import start_from_lobby
from states.treasure.auto_treasure import auto_treasure


class StateEnum(Enum):
    Idle = auto()
    CloseXPopup = auto()
    ConfirmPopup = auto()
    SendLives = auto()
    GetRelic = auto()
    StartFromLobby = auto()
    BuyBoost = auto()
    RandomBoost = auto()
    StartFromBoost = auto()
    InGame = auto()
    MatchEnd = auto()
    OpenBox = auto()
    CookieRelay = auto()
    AutoTreasure = auto()


handler = {
    StateEnum.Idle: idle,
    StateEnum.CloseXPopup: close_x_popup,
    StateEnum.ConfirmPopup: confirm_popup,
    StateEnum.SendLives: send_lives,
    StateEnum.GetRelic: get_relic,
    StateEnum.StartFromLobby: start_from_lobby,
    StateEnum.BuyBoost: buy_boost,
    StateEnum.RandomBoost: buy_random_boost,
    StateEnum.StartFromBoost: start_from_boost,
    StateEnum.InGame: in_game,
    StateEnum.MatchEnd: end_match_ok,
    StateEnum.OpenBox: open_box,
    StateEnum.CookieRelay: cookie_relay,
    StateEnum.AutoTreasure: auto_treasure,
}


@dataclass
class bot_state:
    state: StateEnum = StateEnum.Idle
    coin_count: int = 0

    def update(self, device_id, state):
        emit("state", device=device_id, state=state.name)
        self.state = state

    def update_coin(self, device_id, coin):
        emit("coins", device=device_id, coins=coin)
        self.coin_count = coin

    def run(self, device_id, config, stop_event):

        while not stop_event.is_set():
            handler[self.state](device_id, self, StateEnum, config)
            time.sleep(0.25)
