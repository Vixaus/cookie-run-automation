import time
import threading

from vision.template_match import match_template
from config.config import load_config
from vision.templates import MATCH_END, COOKIE_RELAY, IN_GAME
from automation.auto_jump import auto_jump

def in_game(bot, state_enum):

    time.sleep(5)

    if match_template(IN_GAME["img"], IN_GAME["tl"], IN_GAME["br"]):

        config = load_config()
        cookie_relay = config.get("Cookie_Relay", False)
        auto_jump_enabled = config.get("Auto_Jump", False)

        auto_jump_thread = None

        if auto_jump_enabled:
            auto_jump_thread = threading.Thread(target=auto_jump, daemon=True)
            auto_jump_thread.start()


        if cookie_relay:
            while not match_template(COOKIE_RELAY["img"], COOKIE_RELAY["tl"], COOKIE_RELAY["br"]):
                time.sleep(0.5)
            return bot.update(state_enum.CookieRelay)
        else:
            while not match_template(MATCH_END["img"], MATCH_END["tl"], MATCH_END["br"]):
                time.sleep(0.5)

            if auto_jump_thread is not None:
                auto_jump_thread.join()

            return bot.update(state_enum.MatchEnd)
    else:
        return bot.update(state_enum.StartFromBoost)
