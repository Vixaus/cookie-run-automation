from opencv.template_match import match_template
import time

def idle(bot, state_enum):
   time.sleep(2)
   if match_template("confirm_popup") and bot.state == state_enum.Idle:
      return bot.update(state_enum.ConfirmPopup)
   else:
      return bot.update(state_enum.StartFromLobby)
