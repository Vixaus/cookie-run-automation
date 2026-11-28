# Cookie Run Classic Automation 🍪 (bridge branch)

this branch is the bot that runs inside **Crumble**, my desktop app for Cookie Run Classic. the app has the buttons and settings, and this bot does the actual playing in the background.

**just want to use it? get [Crumble](https://github.com/Vixaus/crumble) instead.** it comes with this bot already, so you don't need anything from here.

the rest of this page is for people building Crumble from source or messing with the bot.

## Main vs bridge

| | `main` | `bridge` (this one) |
| --- | --- | --- |
| how you start it | `python main.py` in a terminal | Crumble starts it for you |
| picking devices | arrow key menu | you tick them in the app |
| settings | edit the json files yourself | edit them in the app |
| output | prints to the terminal | sends JSON lines to the app |
| stopping | `Ctrl+C` | the Stop button (the app sends `stop`) |

## Setup (for Crumble devs)

Crumble wants this repo cloned **next to** it, in a folder called `automation`:

```
some-folder/
  crumble/      the app
  automation/   this repo, on the bridge branch
```

```
git clone https://github.com/Vixaus/crumble.git
git clone -b bridge https://github.com/Vixaus/cookie-run-automation.git automation
```

don't forget the `-b bridge`. without it you get `main`, and the app can't talk to that one.

install the python stuff (InquirerPy isn't needed on this branch):

```
pip install opencv-python numpy easyocr requests
```

then start the app:

```
cd crumble
npm install
npm run tauri dev
```

dev builds run `python main.py` from `../automation`, so any change you make to the bot shows up the next time you press Start. the installed app uses a packaged copy instead (Crumble's `scripts/build-bot.ps1` makes it).

## How the app talks to the bot

the app runs `main.py` with one of these:

| flag | what it does |
| --- | --- |
| `--list-devices` | prints the emulators adb can see, then quits |
| `--default-config` | prints the default settings, then quits |
| `--devices a,b,c` | starts the bot on those devices (comma separated) |
| `--config-dir <folder>` | where to read and save the settings files. the app passes its own folder |

while it runs, the bot prints one JSON object per line on stdout. like this:

```json
{"type": "state", "device": "127.0.0.1:16384", "state": "InGame"}
```

these are all the types:

- `devices`: the list from `--list-devices`
- `default_config`: the settings from `--default-config`
- `started`: the bots are running
- `state`: a device moved to a new step (lobby, boost, in game, etc)
- `coins`: a device's coin count
- `log`: a normal message
- `error`: something broke. after 5 errors in a row that device gives up
- `stopping` / `stopped`: shutting down

to stop it, the app writes `stop` on stdin (or just closes stdin). the bot then has 10 seconds to finish up.

### running it without the app

you can test the bot by itself too:

```
python main.py --devices 127.0.0.1:16384
```

you'll see the JSON lines in the terminal. type `stop` and press enter to end it. without `--config-dir` the settings go in `config/devices_config/`.

## Heads up

- the emulator **has to be 1280x720 at 240 DPI**. other sizes break every tap and screen check
- Windows only (adb comes with the repo in `tools/`)
- the first run is slow because EasyOCR downloads its text reading model

## Settings and how it works

the settings and the bot's steps are the same as on main, so check the [main branch README](https://github.com/Vixaus/cookie-run-automation/tree/main#settings) for the full settings table and the "how it works" part.

## Disclaimer

this is just a side project. it's not made by Devsisters or linked to them in any way. use it at your own risk.

## License

[MIT](LICENSE)
