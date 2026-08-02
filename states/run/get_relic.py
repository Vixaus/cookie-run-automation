from adb.action import ClickAction, click_sequence
from notification.discord_webhook import send_relic_webhook
from utils.use_webhook import use_webhook
from vision.get_text import get_text
from vision.match_template import match_template
from vision.templates import GET_RELIC

claim_action: list[ClickAction] = [
    ClickAction(
        tl=(508, 110),
        br=(561, 117),
        wait=1.5,
    ),
    ClickAction(
        tl=(588, 561),
        br=(691, 604),
        wait=10,
    ),
]

confirm_action: list[ClickAction] = [
    ClickAction(
        tl=(1005, 100),
        br=(1020, 115),
        wait=1,
    ),
    ClickAction(
        tl=(522, 542),
        br=(737, 590),
        wait=1,
    ),
    ClickAction(
        tl=(1062, 151),
        br=(1089, 165),
        wait=1,
    ),
]


def get_relic(device_id, bot, state_enum, config):

    if match_template(device_id, GET_RELIC):
        episode = (get_text(device_id, (324, 77), (343, 98), True) or ["Unknown"])[0]

        click_sequence(device_id, claim_action)

        reward = (get_text(device_id, (350, 430), (950, 515)) or ["Unknown"])[0]

        if use_webhook(config):
            send_relic_webhook(
                {
                    "device_id": device_id,
                    "config": config,
                    "episode": episode,
                    "reward": reward,
                }
            )

        click_sequence(device_id, confirm_action)

    return bot.update(device_id, state_enum.Idle)
