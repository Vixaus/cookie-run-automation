from opencv.template_match import match_template
from adb.action import click

def confirm_popup(bot, state_enum):
    if match_template('confirm_popup') and bot.state == state_enum.ConfirmPopup:
        click((522, 542), (737, 590))
        return bot.update(state_enum.Idle)
