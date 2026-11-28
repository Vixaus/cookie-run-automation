import random
import threading
import time

from adb.action import ClickAction, click, click_sequence
from automation.auto_jump import auto_jump
from utils.wait import wait
from vision.match_template import match_template
from vision.templates import COOKIE_RELAY, FAST_START, IN_GAME, MATCH_END

start_game = {}
timeout = 600


def exceed_timeout(device_id):
    return time.time() - start_game[device_id] >= timeout


def quit_match(device_id, config):

    if not config.get("Quit_Match", False) or not config.get("Quit_Match_At", 0):
        return False

    if time.time() - start_game[device_id] >= config.get("Quit_Match_At", 0):
        print(f"{device_id}: Quitting match...")

        quit_match_action: list[ClickAction] = [
            ClickAction(
                tl=(1118, 30),
                br=(1205, 45),
                wait=random.randint(1, 2),
            ),
            ClickAction(
                tl=(593, 413),
                br=(674, 441),
                wait=random.randint(1, 2),
            ),
            ClickAction(
                tl=(575, 358),
                br=(692, 411),
                wait=random.randint(2, 3),
            ),
        ]

        click_sequence(device_id, quit_match_action)
        return True
    return False


def in_game(device_id, bot, state_enum, config):

    if match_template(device_id, IN_GAME):
        start_game[device_id] = time.time()

        fast_start = config.get("Fast_Start", False)
        cookie_relay = config.get("Cookie_Relay", False)
        auto_jump_enabled = config.get("Auto_Jump", False)
        stop_auto_jump = threading.Event()

        auto_jump_thread = threading.Thread(
            target=auto_jump, args=(device_id, stop_auto_jump, config), daemon=True
        )

        if fast_start:
            # ~10-20 s, then play without it: no Fast Start item left, or a popup covers it.
            for _ in range(50):
                if match_template(device_id, FAST_START):
                    click(device_id, FAST_START["tl"], FAST_START["br"])
                    print(f"{device_id}: Clicked fast start")
                    break
                time.sleep(0.1)

        if auto_jump_enabled:
            wait(1, 3)
            stop_auto_jump.clear()
            auto_jump_thread.start()

        try:
            if cookie_relay:
                while not match_template(device_id, COOKIE_RELAY):
                    if quit_match(device_id, config) or exceed_timeout(device_id):
                        break
                    time.sleep(0.25)

                return bot.update(device_id, state_enum.CookieRelay)

            else:
                while not match_template(device_id, MATCH_END):
                    if quit_match(device_id, config) or exceed_timeout(device_id):
                        break
                    time.sleep(0.25)

                return bot.update(device_id, state_enum.MatchEnd)
        finally:
            # Also on an error: auto-jump must not keep tapping after the run.
            stop_auto_jump.set()
            if auto_jump_thread.is_alive():
                auto_jump_thread.join()
    else:
        return bot.update(device_id, state_enum.StartFromBoost)
