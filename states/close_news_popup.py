from opencv.template_match import match_template
from adb.action import click

def close_news_popup(bot, state_enum):
    if match_template('news_popup') and bot.state == state_enum.CloseNewsPopup:
        click((1114, 82), (1139, 99))
        return bot.update(state_enum.Idle)
