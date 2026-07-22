from vision.template_match import match_template
from config.config import load_config
from vision.text_match import match_text
from vision.templates import X_POPUP, GET_RELIC, LOBBY
import time

def idle(bot, state_enum):
    config = load_config()
    get_relic = config.get("Get_Relic", False)

    time.sleep(1)

    checks = [
        (X_POPUP, state_enum.CloseXPopup),
        (GET_RELIC, state_enum.GetRelic),
        (LOBBY, state_enum.StartFromLobby),
    ]

    if match_text(["confirm", "ok", "cancel"], (390, 400), (870, 710)):
            return bot.update(state_enum.ConfirmPopup)

    for template_name, next_state in checks:
        if match_template(template_name["img"], template_name["tl"], template_name["br"]):
            if (template_name == "get_relic" and get_relic) or (template_name != "get_relic") :
                return bot.update(next_state)

    return bot.update(state_enum.OpenBox)
