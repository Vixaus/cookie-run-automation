import threading

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from adb.device import online_devices
from config.config import create_config, default_config, load_config
from states.base import bot_state

selected_devices = []


def ask_user_prompt():

    device_choice = [Choice(value="All", enabled=True)]

    for device in online_devices:
        device_choice.append(Choice(value=device))

    user_prompt = inquirer.checkbox(
        message="Select devices to start the bot (use space to select, arrow keys to navigate, enter to confirm)\n\n",
        choices=device_choice,
        default=["All"],
        validate=lambda result: len(result) == 1 if "All" in result else True,
        invalid_message="You can't select both 'All' and individual devices",
    ).execute()

    answer = user_prompt

    # print(f"\nSelected devices: {answer if answer != ['All'] else 'All'}\n")

    if answer == ["All"]:
        return online_devices
    else:
        return answer or []


def start_bot(device_id, config):
    bot = bot_state()
    bot.run(device_id, config)


def start():
    global selected_devices
    selected_devices = ask_user_prompt()

    for device_id in selected_devices:
        config = load_config(device_id)

        if not config or not set(default_config).issubset(set(config)):
            print(f"\n{device_id}: Created new config")
            config = create_config(device_id)

        print(f"\n{device_id}: Is starting...")
        thread = threading.Thread(target=start_bot, args=(device_id, config))
        thread.start()
