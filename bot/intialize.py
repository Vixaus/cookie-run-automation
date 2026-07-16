import time

from states.base import bot_state
from states.select_boost import select_boost
from states.start_game import start_game

bot = bot_state()
while True:
    bot.update(start_game())
    time.sleep(2)
    bot.update(select_boost())
