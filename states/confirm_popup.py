from vision.text_match import match_text
from adb.action import click

def confirm_popup(bot, state_enum):

    matched_pos = match_text(['confirm', 'ok', "cancel"], (300, 410), (940, 700))
    x, y, _ = matched_pos or (0, 0, "")

    if matched_pos and bot.state == state_enum.ConfirmPopup:
        click((x - 10, y - 10), (x + 10, y + 10))

    return bot.update(state_enum.Idle)
