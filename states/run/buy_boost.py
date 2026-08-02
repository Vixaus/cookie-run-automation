import time

from adb.action import click
from vision.match_template import match_color, match_template
from vision.templates import BOOST

boost_type = {"Hp": (173, 392), "Power": (327, 392), "Xp": (534, 392)}


def buy_boost(device_id, bot, state_enum, config):
    random_boost = config.get("Buy_Random_Boost", False)
    wl = config.get("Selected_Boost", {})

    if match_template(device_id, BOOST):
        for boost, value in boost_type.items():
            boost_state = wl.get(boost, False)
            tl = (value[0] - 5, value[1] - 5)
            br = (value[0] + 5, value[1] + 5)

            if (
                boost_state
                and not match_color(device_id, (253, 225, 0), value)
                or not boost_state
                and match_color(device_id, (253, 225, 0), value)
            ):
                click(device_id, tl, br)

            time.sleep(0.5)

        if random_boost:
            return bot.update(device_id, state_enum.RandomBoost)
        return bot.update(device_id, state_enum.StartFromBoost)

    return bot.update(device_id, state_enum.StartFromLobby)
