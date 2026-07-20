from vision.text_match import match_text
from adb.action import click

def confirm_popup(bot, state_enum):

    matched_pos = match_text(['confirm', 'ok'], (390, 400), (870, 710))
    x, y = matched_pos or (0, 0)

    print(f"clicked at {(x - 10, y - 10), (x + 10, y + 10)}")

    if matched_pos and bot.state == state_enum.ConfirmPopup:
        click((x - 10, y - 10), (x + 10, y + 10))

    return bot.update(state_enum.Idle)
