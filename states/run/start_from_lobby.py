import time

from adb.action import click
from vision.match_template import match_template
from vision.templates import LOBBY


def start_from_lobby(device_id, bot, state_enum, config):
    buy_boost = config.get("Buy_Boost", False)
    buy_multi_boost = config.get("Buy_Random_Boost", False)

    next_boost = [
        (buy_boost, state_enum.BuyBoost),
        (buy_multi_boost, state_enum.RandomBoost),
    ]

    if match_template(
        device_id,
        LOBBY,
    ):
        click(device_id, (807, 619), (1112, 668))
        time.sleep(2)
        for selected, state in next_boost:
            if selected:
                return bot.update(device_id, state)
        return bot.update(device_id, state_enum.StartFromBoost)
    else:
        return bot.update(device_id, state_enum.Idle)
