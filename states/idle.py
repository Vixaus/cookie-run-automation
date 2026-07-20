from vision.template_match import match_template
from utils.config import load_config
from vision.text_match import match_text
from utils.templates import CLOSE_X_POPUP, GET_RELIC, LOBBY_TEMPLATE
import time

def idle(bot, state_enum):
    config = load_config()
    get_relic = config.get("Get_Relic", False)

    time.sleep(1)

    checks = [
        (CLOSE_X_POPUP, state_enum.CloseXPopup),
        (GET_RELIC, state_enum.GetRelic),
        (LOBBY_TEMPLATE, state_enum.StartFromLobby),
    ]

    if match_text(["confirm", "ok"], (390, 400), (870, 710)):
        return bot.update(state_enum.ConfirmPopup)

    for template_name, next_state in checks:
        if match_template(template_name):
            if (template_name == "get_relic" and get_relic) or (template_name != "get_relic") :
                return bot.update(next_state)

    print("in this loop")

    return False
