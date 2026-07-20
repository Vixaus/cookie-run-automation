import time
from vision.template_match import match_template
from adb.action import click
from utils.templates import COOKIE_RELAY, MATCH_END

def cookie_relay(bot, state_enum):
    if match_template(COOKIE_RELAY) and bot.state == state_enum.CookieRelay:
        click((591,285), (700,395))

        while not match_template(MATCH_END):
            time.sleep(0.5)
        return bot.update(state_enum.MatchEnd)

    return bot.update(state_enum.InGame)
