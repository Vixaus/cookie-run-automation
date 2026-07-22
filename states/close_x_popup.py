from vision.template_match import match_template
from adb.action import click
from vision.templates import X_POPUP

def close_x_popup(bot, state_enum):

    matched_pos = match_template(X_POPUP['img'], X_POPUP['tl'], X_POPUP['br'])
    x, y = matched_pos or (0, 0)

    if matched_pos and bot.state == state_enum.CloseXPopup:
        click((x - 10, y - 10), (x + 10, y + 10))

    return bot.update(state_enum.Idle)
