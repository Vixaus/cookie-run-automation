from adb.action import click
from vision.match_text import match_text


def confirm_popup(device_id, bot, state_enum, _):

    matched_pos = match_text(
        device_id, ["confirm", "conficm", "ok", "cancel"], (300, 410), (940, 700)
    )
    x, y, _ = matched_pos or (0, 0, "")

    if matched_pos:
        click(device_id, (x - 5, y - 5), (x + 10, y + 10))

    return bot.update(device_id, state_enum.Idle)
