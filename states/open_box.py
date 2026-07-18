from opencv.template_match import match_template
from adb.action import click_position
import time

def open_box(bot, state_enum):
   if match_template("open_box") and bot.state == state_enum.OpenBox:

      for _ in range(2):
         time.sleep(1)
         click_position((528,621), (742,655))

   return bot.update(state_enum.Idle)
