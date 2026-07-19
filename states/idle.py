from opencv.template_match import match_template
from utils.load_config import load_config
import time

def idle(bot, state_enum):
    config = load_config()
    get_relic = config.get("Get_Relic", False)

    time.sleep(1)

    checks = [
        ("x_popup", state_enum.CloseXPopup),
        ("confirm_reward", state_enum.ConfirmReward),
        ("confirm_league", state_enum.ConfirmLeague),
        ("get_relic", state_enum.GetRelic),
        ("lobby", state_enum.StartFromLobby),
    ]

    for template_name, next_state in checks:
        if match_template(template_name):
            if (template_name == "get_relic" and get_relic) or (template_name != "get_relic") :
                return bot.update(next_state)

    return False
