import time
from vision.template_match import match_template
from adb.action import click
from vision.templates import COOKIE_RELAY, MATCH_END
from config.config import load_config
from automation.auto_jump import auto_jump
import threading

def cookie_relay(bot, state_enum):
    if match_template(COOKIE_RELAY["img"], COOKIE_RELAY.get("tl"), COOKIE_RELAY.get("br")) and bot.state == state_enum.CookieRelay:

        time.sleep(1)
        click((591,285), (700,395))

        config = load_config()
        auto_jump_enabled = config.get("Auto_Jump", False)
        stop_auto_jump = threading.Event()

        auto_jump_thread = threading.Thread(target=auto_jump, args=(stop_auto_jump,), daemon=True)

        if auto_jump_enabled:
            stop_auto_jump.clear()
            auto_jump_thread.start()

        while not match_template(MATCH_END["img"], MATCH_END.get("tl"), MATCH_END.get("br")):
            time.sleep(0.5)

        if auto_jump_enabled:
            stop_auto_jump.set()
            auto_jump_thread.join()

        return bot.update(state_enum.MatchEnd)

    return bot.update(state_enum.InGame)
