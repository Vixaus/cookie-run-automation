from opencv.template_match import match_template
from adb.action import click

def close_x_popup(bot, state_enum):

    matched_pos = match_template('x_popup')
    x, y = matched_pos or (0, 0)

    if matched_pos and bot.state == state_enum.CloseXPopup:
        click((x - 10, y - 10), (x + 10, y + 10))
        return bot.update(state_enum.Idle)
    return False
