import threading
from copy import deepcopy
from datetime import datetime
from typing import TypedDict

import requests


class AutoRunWebhook(TypedDict):
    device_id: str
    config: dict
    time: str
    result_coins: int
    total_coins: int
    xp: int
    box: int


class AutoTreasureWebhook(TypedDict):
    device_id: str
    config: dict
    magic_powder: int
    total_powder: int
    current_coin: int


class RelicWebhook(TypedDict):
    device_id: str
    config: dict
    episode: str
    reward: str


message = {
    "content": None,
    "embeds": [
        {
            "title": "",
            "description": "",
            "color": 8799744,
            "footer": {
                "text": "Cookie Run Classic",
                "icon_url": "https://play-lh.googleusercontent.com/tqhrRxdTKQIFKKXVNIU0xVeMJG6oFNvwexB_N1mZC181-x_KmJBP3FNgWqsPU7OwGKwr3Dkvld9-7FDzkAjhnrM",
            },
            "timestamp": None,
            "image": {
                "url": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbTF5aGRmNXJtbGhnZmtmZGxwZmNudnpzbjF2d3R2c2E0NXhvbHdzMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/i8mLz76H5tEtj5obvI/giphy.gif"
            },
        }
    ],
    "attachments": [],
}


def webhook_url(config):
    url = config.get("Webhook_URL", None)

    return url


def get_timestamp():
    return datetime.now().astimezone().isoformat()


def handle_webhook(device_id, url, local_message):
    try:
        response = requests.post(url, json=local_message, timeout=10)
        response.raise_for_status()
        print(f"{device_id}: Webhook sent successfully")

    except requests.RequestException as error:
        # Not str(error): requests puts the webhook URL, token included, in it.
        why = (
            error.response.status_code
            if error.response is not None
            else type(error).__name__
        )
        print(f"{device_id}: Failed to send webhook ({why})")


def relic_typo_fix(reward):
    if len(reward) == 1:
        return f"{reward} Key"
    elif "Coins" in reward:
        return reward.maketrans({"u": "0", "o": "0", "I": "1", "T": "1", "Z": "2"})
    elif "Ticket" in reward:
        return reward.replace("|", "T")
    elif "Received" in reward:
        return reward[:-1]
    elif "Powder" in reward:
        return reward.replace("L,oou", "1,000")
    else:
        return reward


def send_run_webhook(AutoRun: AutoRunWebhook):

    device_id = AutoRun["device_id"]

    is_1_minute = AutoRun["time"].split(":")[0][-1] == "1"
    is_1_box = AutoRun["box"] == 1

    url = webhook_url(AutoRun["config"])
    local_message = deepcopy(message)
    local_message["embeds"][0]["title"] = "Match End Results"
    local_message["embeds"][0]["description"] = f" \
        **Device Id**: ||{device_id}|| \
        \n\n **Time Taken** \n {AutoRun['time']} {'minute' if is_1_minute else 'minutes'} \
        \n\n **Rewards** \n + {AutoRun['result_coins']:,} coins\n + {AutoRun['xp']:,} xp {f'\n + {AutoRun['box']} {'box' if is_1_box else 'boxes'}' if AutoRun['box'] else ''} \
        \n\n **Total Coins** \n x{AutoRun['total_coins']:,}"
    local_message["embeds"][0]["timestamp"] = get_timestamp()

    thread = threading.Thread(
        target=handle_webhook, args=(device_id, url, local_message), daemon=True
    )
    thread.start()


def send_treasure_webhook(AutoTreasure: AutoTreasureWebhook):

    device_id = AutoTreasure["device_id"]

    url = webhook_url(AutoTreasure["config"])
    local_message = deepcopy(message)
    local_message["embeds"][0]["title"] = "Auto Treasure Results"
    local_message["embeds"][0]["description"] = f" \
        **Device Id**: ||{device_id}|| \
        \n\n **Rewards** \n + {AutoTreasure['magic_powder']:,} magic powder \
        \n\n **Total Powders** \n x{AutoTreasure['total_powder']:,} \
        \n\n **Total Coins** \n x{AutoTreasure['current_coin']:,}"
    local_message["embeds"][0]["timestamp"] = get_timestamp()

    thread = threading.Thread(
        target=handle_webhook, args=(device_id, url, local_message), daemon=True
    )
    thread.start()


def send_relic_webhook(AutoRelic: RelicWebhook):

    reward = relic_typo_fix(AutoRelic["reward"])

    device_id = AutoRelic["device_id"]

    url = webhook_url(AutoRelic["config"])
    local_message = deepcopy(message)
    local_message["content"] = "@everyone"
    local_message["embeds"][0]["title"] = f"Episode {AutoRelic['episode']} Relic Result"
    local_message["embeds"][0]["description"] = f" \
        **Device Id**: ||{device_id}|| \
        \n\n **Rewards** \n + {reward}"
    local_message["embeds"][0]["timestamp"] = get_timestamp()

    thread = threading.Thread(
        target=handle_webhook, args=(device_id, url, local_message), daemon=True
    )
    thread.start()
