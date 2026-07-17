import threading
import time

from states.base import bot_state, state_enum

bot = bot_state()

while True:
    bot.update(state_enum.StartFromLobby)
