import json
from pathlib import Path

from automation.bridge import emit

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

# Where per-device config files live. The Tauri app passes its own writable
# folder with --config-dir; running main.py by hand uses the folder next to this file.
config_dir = Path(__file__).parent / "devices_config"


def set_config_dir(path):
    global config_dir
    config_dir = Path(path)


def config_file(device_id):
    """Network devices like 127.0.0.1:16384 (MuMu) have a ':', which Windows file
    names can't contain. Same rule as config_path in the app's lib.rs."""
    return config_dir / f"{device_id.replace(':', '_')}.json"


def load_config(device_id):
    try:
        with open(config_file(device_id), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        emit("log", device=device_id, msg="No config file found.")
        return {}


def create_config(device_id):
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_file(device_id), "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4)
    emit("log", device=device_id, msg="Created new config.")
    return dict(default_config)
