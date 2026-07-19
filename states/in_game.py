import time

from opencv.template_match import match_template
from utils.load_config import load_config

def in_game(bot, state_enum):
    config = load_config()
    cookie_relay = config.get("Cookie_Relay", False)
    if cookie_relay:
        while not match_template("cookie_relay"):
            time.sleep(0.5)
        return bot.update(state_enum.CookieRelay)
    else:
        while not match_template("end_ok"):
            time.sleep(1)
        return bot.update(state_enum.MatchEnd)
