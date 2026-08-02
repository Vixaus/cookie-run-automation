import threading
import time

from adb.action import click
from automation.auto_jump import auto_jump
from states.run.in_game import exceed_timeout, quit_match
from utils.wait import wait
from vision.match_template import match_template
from vision.templates import COOKIE_RELAY, MATCH_END


def click_cookie_relay(device_id):
    time.sleep(0.25)
    click(device_id, COOKIE_RELAY["tl"], COOKIE_RELAY["br"])


def cookie_relay(device_id, bot, state_enum, config):
    if quit_match(device_id, config) or exceed_timeout(device_id):
        return bot.update(device_id, state_enum.MatchEnd)

    thread = threading.Thread(target=click_cookie_relay, args=(device_id,))
    thread.start()

    if match_template(device_id, COOKIE_RELAY):
        wait(1, 2)

        auto_jump_enabled = config.get("Auto_Jump", False)
        stop_auto_jump = threading.Event()

        auto_jump_thread = threading.Thread(
            target=auto_jump,
            args=(device_id, stop_auto_jump, config),
            daemon=True,
        )

        if auto_jump_enabled:
            stop_auto_jump.clear()
            auto_jump_thread.start()

        while not match_template(device_id, MATCH_END):
            if quit_match(device_id, config) or exceed_timeout(device_id):
                break
            time.sleep(0.25)

        if auto_jump_enabled:
            stop_auto_jump.set()
            auto_jump_thread.join()

        return bot.update(device_id, state_enum.MatchEnd)

    return bot.update(device_id, state_enum.InGame)
