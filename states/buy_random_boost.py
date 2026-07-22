import time

from vision.template_match import match_template, match_color
from adb.action import click_sequence, ClickAction
from vision.templates import BOOST
from config.config import load_config


def buy_random_boost(bot, state_enum):

    config = load_config()
    buy_boost = config.get('Buy_Boost', False)

    actions: list[ClickAction] = [
        ClickAction(
            tl=(486, 544),
            br=(583, 647),
            wait=1,
        ),
        ClickAction(
            tl=(1070, 178),
            br=(1120, 208),
            wait=1,
        ),
        ClickAction(
            tl=(545, 570),
            br=(716, 609),
            wait=1,
        ),
    ]

    if match_template(BOOST["img"], BOOST["tl"], BOOST["br"]) and bot.state == state_enum.RandomBoost:
        click_sequence(actions)

        while match_color((78, 77, 75), (140, 330)):
           time.sleep(1)

        return bot.update(state_enum.StartFromBoost)
    elif buy_boost:
        return bot.update(state_enum.BuyBoost)
    else:
        return bot.update(state_enum.StartFromLobby)
