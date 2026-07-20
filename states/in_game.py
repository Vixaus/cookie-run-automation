import time

from vision.template_match import match_template
from utils.config import load_config
from utils.templates import MATCH_END, COOKIE_RELAY, IN_GAME

def in_game(bot, state_enum):


    if match_template(IN_GAME):
        config = load_config()
        cookie_relay = config.get("Cookie_Relay", False)
        if cookie_relay:
            while not match_template(COOKIE_RELAY):
                time.sleep(0.5)
            return bot.update(state_enum.CookieRelay)
        else:
            while not match_template(MATCH_END):
                time.sleep(0.5)
            return bot.update(state_enum.MatchEnd)
    else:
        return bot.update(state_enum.StartFromBoost)
