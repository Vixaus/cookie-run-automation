import time

from vision.template_match import match_color, match_template
from adb.action import click
from utils.config import load_config
from utils.templates import BOOST

boost_type = {
    "Hp": (173,392),
    "Power": (327,392),
    "Xp": (534, 392)
}

def check_boost(boost):
    for b in boost:
        if match_color((253, 225, 0), boost_type[b]):
            return True
    return False


def buy_boost(bot, state_enum):
    config = load_config()
    multi_boost = config.get("Buy_Multi_Boost", False)
    wl = config.get("Selected_Boost", {})

    if match_template(BOOST) and bot.state == state_enum.BuyBoost:
        for boost in boost_type:
            boost_state = wl.get(boost, False)
            tl = (boost_type[boost][0] - 5, boost_type[boost][1] - 5)
            br = (boost_type[boost][0] + 5, boost_type[boost][1] + 5)

            if boost_state and not match_color((253, 225, 0), boost_type[boost]):
                click(tl, br)
            elif not boost_state and match_color((253, 225, 0), boost_type[boost]):
                click(tl, br)

            time.sleep(1)

        if multi_boost:
            return bot.update(state_enum.RandomBoost)
        return bot.update(state_enum.StartFromBoost)

    return bot.update(state_enum.StartFromLobby)
