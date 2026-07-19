from opencv.template_match import match_template
from adb.action import click

def confirm_reward(bot, state_enum):

    matched_pos = match_template('confirm_reward')
    x, y = matched_pos or (0, 0)

    if matched_pos and bot.state == state_enum.ConfirmReward:
        click((x - 10, y - 10), (x + 10, y + 10))
        return bot.update(state_enum.Idle)
    return False

def confirm_league(bot, state_enum):
    matched_pos = match_template('confirm_league')
    x, y = matched_pos or (0, 0)

    if matched_pos and bot.state == state_enum.ConfirmLeague:
        click((x - 10, y - 10), (x + 10, y + 10))
        return bot.update(state_enum.Idle)
    return False
