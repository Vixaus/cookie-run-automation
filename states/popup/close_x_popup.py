from adb.action import click
from vision.match_template import match_template
from vision.templates import X_POPUP


def close_x_popup(device_id, bot, state_enum, _):

    matched_pos = match_template(device_id, X_POPUP)
    x, y = matched_pos or (0, 0)

    if matched_pos:
        click(device_id, (x - 10, y - 10), (x + 10, y + 10))

    return bot.update(device_id, state_enum.Idle)
