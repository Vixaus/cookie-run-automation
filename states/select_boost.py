from opencv.template_match import match_template, match_color
from adb.action import click_position
from utils.wait import wait

def select_boost(bot, state_enum):
    if match_template("boost") and bot.state == state_enum.SelectBoost:
        print("buying Multi Boost")
        click_position((486, 544),(583,647))
        wait(1,2)
        click_position((1070, 178), (1120, 208))
        wait(1,2)
        click_position((545, 570), (716, 609))
        wait(1,2)

        print("waiting for power plus")
        while match_color((78, 77, 75), (140, 330)):
           wait(1, 1.5)

        print("power plus found")
        return bot.update(state_enum.StartFromBoost)
    else:
        print("boost screen not found")
