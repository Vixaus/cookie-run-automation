import time

from adb.action import click
from utils.get_coins import get_coins
from utils.use_webhook import use_webhook
from vision.match_template import match_template
from vision.templates import START_GAME


def update_coin(device_id, bot):
    coin = get_coins(device_id)
    bot.update_coin(device_id, coin)


def start_from_boost(device_id, bot, state_enum, config):

    if match_template(device_id, START_GAME):
        if use_webhook(config):
            update_coin(device_id, bot)

        click(device_id, (794, 601), (1020, 629))
        time.sleep(4)

        return bot.update(device_id, state_enum.InGame)
    else:
        return bot.update(device_id, state_enum.StartFromLobby)
