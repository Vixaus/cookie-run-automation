import time

from adb.action import click
from notification.discord_webhook import send_run_webhook
from states.run.in_game import start_game
from utils.use_webhook import use_webhook
from vision.get_text import get_text
from vision.match_template import match_color, match_template
from vision.templates import MATCH_END, OPEN_BOX


def send_webhook(device_id, bot, config):
    print(f"{device_id}: Sending webhook...")

    elapsed = int(time.time() - start_game.get(device_id, 0))
    time_elapsed = f"{elapsed // 60}:{elapsed % 60:02d}"

    result = get_text(device_id, (950, 390), (1130, 520), True) or ["0", "0"]

    result_coin = int(result[0].replace(",", "") or "0")
    total_coin = bot.coin_count + result_coin

    result_exp = int(result[1].replace(",", "") or "0") if len(result) > 1 else 0

    total_box = (get_text(device_id, (1088, 212), (1124, 257), True))[0]
    box = 1 if total_box == "J" else (3 if total_box == "8" else int(total_box))

    send_run_webhook(
        {
            "device_id": device_id,
            "config": config,
            "time": time_elapsed,
            "result_coins": result_coin,
            "total_coins": total_coin,
            "xp": result_exp,
            "box": box,
        }
    )


def end_match_ok(device_id, bot, state_enum, config):

    if match_template(device_id, MATCH_END) and match_color(
        device_id, (240, 239, 234), (163, 223)
    ):
        if use_webhook(config):
            time.sleep(5)
            send_webhook(device_id, bot, config)

        click(device_id, (415, 600), (513, 641))
        time.sleep(1)

        if match_template(device_id, OPEN_BOX):
            return bot.update(device_id, state_enum.OpenBox)
        else:
            return bot.update(device_id, state_enum.Idle)

    else:
        return bot.update(device_id, state_enum.InGame)
