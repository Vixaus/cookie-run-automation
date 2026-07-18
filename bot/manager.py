import time
from states.base import bot_state, state_enum

bot = bot_state()

while True:
   time.sleep(1)
   bot.update(state_enum.Idle)
