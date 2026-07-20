from vision.template_match import match_template
from adb.action import click
from utils.templates import START_GAME


def start_from_boost(bot, state_enum):
    if match_template(START_GAME) and bot.state == state_enum.StartFromBoost:
        click((794, 601), (1020, 629))
        return bot.update(state_enum.InGame)
    else:
        return False
