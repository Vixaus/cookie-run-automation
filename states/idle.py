from vision.get_text import get_text
from vision.match_template import match_template
from vision.match_text import match_text
from vision.templates import GET_RELIC, LOBBY, X_POPUP


def check_relic(template_name, get_relic):
    return (template_name["img"] == "get_relic" and get_relic) or (
        template_name["img"] != "get_relic"
    )


def send_lives(device_id, config):
    send_lives = config.get("Send_Lives", False)
    send_lives_at = config.get("Send_Lives_At", 0)

    if send_lives:
        mail_noti = (get_text(device_id, (695, 645), (731, 663), True))[0]

        if int(mail_noti) >= send_lives_at:
            print(
                f"{device_id}: Mail is at {int(mail_noti)} your config is {send_lives_at}, start sending lives..."
            )
            return True

    return False


def auto_run(device_id, bot, state_enum, config):
    get_relic = config.get("Get_Relic", False)

    checks = [
        (X_POPUP, state_enum.CloseXPopup),
        (GET_RELIC, state_enum.GetRelic),
        (LOBBY, state_enum.StartFromLobby),
    ]

    for template_name, next_state in checks:
        if match_template(device_id, template_name) and check_relic(
            template_name, get_relic
        ):
            if template_name["img"] == "lobby" and send_lives(device_id, config):
                return bot.update(device_id, state_enum.SendLives)

            return bot.update(device_id, next_state)

    return bot.update(device_id, state_enum.OpenBox)


def auto_treasure(device_id, bot, state_enum, _):
    return bot.update(device_id, state_enum.AutoTreasure)


mode = {"Auto_Run": auto_run, "Auto_Treasure": auto_treasure}


def idle(device_id, bot, state_enum, config):
    selected_mode = config.get("Mode", "Auto_Run")

    _, _, text = match_text(
        device_id, ["confirm", "conficm", "ok", "cancel"], (300, 410), (940, 700)
    )

    if text:
        return bot.update(device_id, state_enum.ConfirmPopup)

    mode[selected_mode](device_id, bot, state_enum, config)
