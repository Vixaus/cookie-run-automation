from opencv.template_match import match_template
from adb.action import click_sequence, ClickAction

def get_relic(bot, state_enum):
    actions: list[ClickAction] = [
        ClickAction(
            tl=(508, 110),
            br=(561, 117),
            wait=1.5,
        ),
        ClickAction(
            tl=(544, 563),
            br=(735, 596),
            wait=5,
        ),
        ClickAction(
            tl=(522, 542),
            br=(737, 590),
            wait=1.5,
        ),
        ClickAction(
            tl=(1062, 151),
            br=(1089, 165),
            wait=1.5,
        ),
    ]

    if match_template("get_relic") and bot.state == state_enum.GetRelic:
        click_sequence(actions)

        return bot.update(state_enum.Idle)
    return False
