from vision.template_match import match_template
from adb.action import click
from utils.wait import wait
from vision.templates import MATCH_END, OPEN_BOX
from config.config import load_config


def end_match_ok(bot, state_enum):
    config = load_config()
    cookie_relay = config.get('Cookie_Relay', False)

    if match_template(MATCH_END["img"], MATCH_END["tl"], MATCH_END["br"]) and bot.state == state_enum.MatchEnd:

       click((350,600), (555,635))
       wait(1,2)
       if match_template(OPEN_BOX["img"], OPEN_BOX["tl"], OPEN_BOX["br"]):
           return bot.update(state_enum.OpenBox)
       else:
           return bot.update(state_enum.Idle)

    elif cookie_relay:
        return bot.update(state_enum.CookieRelay)
    else:
        return bot.update(state_enum.InGame)
