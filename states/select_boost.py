import time

from opencv.template_match import match_template, match_color
from adb.action import click_sequence, ClickAction

def select_boost(bot, state_enum):

    actions: list[ClickAction] = [
        ClickAction(
            tl=(486, 544),
            br=(583, 647),
            wait=1,
        ),
        ClickAction(
            tl=(1070, 178),
            br=(1120, 208),
            wait=1,
        ),
        ClickAction(
            tl=(545, 570),
            br=(716, 609),
            wait=1,
        ),
    ]

    if match_template("boost") and bot.state == state_enum.SelectBoost:
        print("buying multi boost")
        click_sequence(actions)

        print("waiting for power plus")
        while match_color((78, 77, 75), (140, 330)):
           time.sleep(1)

        print("power plus found")
        return bot.update(state_enum.StartFromBoost)
    else:
        print("boost screen not found")
