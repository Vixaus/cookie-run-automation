import time

from adb.action import click
from vision.match_template import match_color, match_template
from vision.templates import CLAIM_LIVES, SEND_LIVES


def send_lives(device_id, bot, state_enum, _):

    click(device_id, (672, 669), (679, 685))
    time.sleep(2)

    start_time = time.time()

    while True:
        send_found = match_template(device_id, SEND_LIVES)
        claim_found = match_template(device_id, CLAIM_LIVES)

        if send_found or claim_found:
            break

        if time.time() - start_time > 10:
            print(f"{device_id}: Time out, cannot find send lives button")
            break

        time.sleep(0.5)

    if match_template(device_id, SEND_LIVES) or match_template(device_id, CLAIM_LIVES):
        click(device_id, (535, 588), (730, 633))
        time.sleep(1)

        while match_color(device_id, (73, 71, 67), (150, 200)):
            click(device_id, (663, 442), (691, 467))
            time.sleep(1)

        click(device_id, (1115, 77), (1142, 102))

    print(f"{device_id}: Send lives completed, exiting...")
    return bot.update(device_id, state_enum.Idle)
