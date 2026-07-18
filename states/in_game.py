from opencv.template_match import match_template
import time

def in_game(bot, state_enum):
    while not match_template("end_ok"):
       time.sleep(1)
    return bot.update(state_enum.MatchEnd)
