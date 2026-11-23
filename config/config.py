import json
from pathlib import Path

default_config = {
    "Mode": "Auto_Run",
    "Auto_Jump": True,
    "Auto_Jump_Delay": [0.1, 0.8],
    "Selected_Boost": {"Hp": True, "Power": True, "Xp": True},
    "Buy_Boost": True,
    "Selected_Random_Boost": ["Double Coins"],
    "Buy_Random_Boost": True,
    "Fast_Start": False,
    "Cookie_Relay": True,
    "Send_Lives": False,
    "Send_Lives_At": 50,
    "Get_Relic": False,
    "Result_Webhook": False,
    "Quit_Match": False,
    "Quit_Match_At": 0,
    "Keep_Choc_Cookie": False,
    "Webhook_URL": "",
}

file_path = Path(__file__).parent / "devices_config"


def config_file(device_id: str) -> Path:
    """Windows forbids ':' in file names, so '127.0.0.1:16384' -> '127.0.0.1_16384.json'."""
    return file_path / f"{device_id.replace(':', '_')}.json"


def load_config(device_id):
    try:
        with open(config_file(device_id), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{device_id}: No config file found.")
        return {}


def create_config(device_id):
    try:
        with open(config_file(device_id), "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
            return default_config
    except FileNotFoundError:
        print(f"{device_id}: No config file found.")
        return {}
