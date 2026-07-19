from opencv.template_match import match_template
from adb.action import click
from utils.wait import wait

def end_match_ok(bot, state_enum):
    if match_template("end_ok") and bot.state == state_enum.MatchEnd:
       click((350,600), (555,635))
       wait(1,2)
       if match_template("open_box"):
           return bot.update(state_enum.OpenBox)
       else:
           return bot.update(state_enum.Idle)
    return False
