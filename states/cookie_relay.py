import time
from opencv.template_match import match_template
from adb.action import click

def cookie_relay(bot, state_enum):
    if match_template("cookie_relay") and bot.state == state_enum.CookieRelay:
        click((591,285), (700,395))

        while not match_template("end_ok"):
            time.sleep(1)
        return bot.update(state_enum.MatchEnd)
    return False
