# Cookie Run Classic Automation 🍪

I made this because grinding coins in Cookie Run Classic by hand is super boring. so now the bot plays for me.

it runs on an android emulator on your pc. it takes screenshots of the game, looks for buttons, and taps them for you. it can run on more than one emulator at the same time too.

## What it can do

- **Auto Run**: starts a run from the lobby, picks your boosts, jumps for you, does cookie relay, ends the run, opens the box, then does it all again
- **Auto Treasure**: draws treasures until your inventory is full, extracts them for magic powder, and repeats
- buys normal boosts (Hp / Power / Xp)
- keeps rerolling the random boost until you get the one you want
- sends lives from the mail when it gets full
- claims relics
- closes random popups
- sends your results to a Discord channel (webhook)

## What you need

- Windows (adb comes with the repo in `tools/`, so you don't need to install it)
- Python 3.12 or newer
- an emulator. i tested it on **LDPlayer** and **MuMu**
- Cookie Run Classic installed on the emulator

install the python stuff:

```
pip install InquirerPy opencv-python numpy easyocr requests
```

## How to run

1. open your emulator and the game, then go to the lobby
2. open a terminal in this folder (the main folder, not a sub folder)
3. run:

   ```
   python main.py
   ```

4. pick your devices. arrow keys to move, space to select, enter to start. `All` picks every device
5. the first time, the bot makes a settings file for each device. stop it with `Ctrl+C`, change the settings (see below), then run it again

the first run can be slow because EasyOCR downloads its text reading model.

## Settings

each device gets its own file in `config/devices_config/`. the name is the device id, with `:` changed to `_`. so `127.0.0.1:16384` becomes `127.0.0.1_16384.json`.

| setting | what it does |
| --- | --- |
| `Mode` | `"Auto_Run"` or `"Auto_Treasure"` |
| `Auto_Jump` | taps jump for you during the run |
| `Auto_Jump_Delay` | `[min, max]` seconds between jumps (it picks a random time in between) |
| `Buy_Boost` | turn on the normal boosts |
| `Selected_Boost` | which normal boosts you want: `Hp`, `Power`, `Xp` (true / false) |
| `Buy_Random_Boost` | keep rerolling the random boost until you get one from your list |
| `Selected_Random_Boost` | your list, like `["Double Coins"]`. type the names exactly like the game shows them |
| `Fast_Start` | taps fast start at the start of the run |
| `Cookie_Relay` | taps the cookie relay button when it shows up |
| `Send_Lives` | sends lives from the mail |
| `Send_Lives_At` | how many mails before it sends lives |
| `Get_Relic` | claims the relic when it shows up |
| `Quit_Match` | quits the run early |
| `Quit_Match_At` | how many seconds before it quits (`0` = never) |
| `Keep_Choc_Cookie` | in Auto Treasure, it won't extract treasures with the choc cookie on them |
| `Result_Webhook` | sends results to Discord |
| `Webhook_URL` | your Discord webhook link |

⚠️ boosts, rerolls and treasure draws cost coins. Auto Treasure spends 5,000 coins per draw, so check your settings before you leave it running.

## How it works

the bot is a loop. each step looks at the screen, does one thing, then picks the next step.

**Auto Run:**

1. **Idle**: looks at the screen to see where we are. a popup? the lobby? a relic?
2. **Lobby**: taps play
3. **Boosts**: picks the boosts you turned on, and rerolls the random boost if you want that
4. **Start**: taps start
5. **In game**: spams jump (if it's on) and waits for cookie relay or the end screen
6. **Cookie relay**: taps relay, keeps jumping, waits for the end screen
7. **End screen**: reads your coins and xp, sends the Discord message, taps ok
8. **Box**: opens the box if there is one
9. back to step 1 🔁

if a run goes over 10 minutes, the bot gives up on it and moves on.

**Auto Treasure** (you have to start in the lobby):

1. opens the treasure menu and reads how much space you have
2. draws treasures until it's full
3. opens extract and taps each treasure until it hits a locked one
4. extracts and reads how much magic powder you got
5. repeats until the treasure button is gone or the game disconnects

**How it "sees" stuff:**

- `vision/templates/` has small pictures of buttons. the bot finds them on the screen with OpenCV
- for text and numbers (coins, mail count, boost names) it uses EasyOCR
- taps go through adb, and each tap lands on a random spot inside the button

## Heads up

- the emulator **has to be 1280x720 at 240 DPI**. other sizes break every tap and screen check
- Windows only (because of `tools/adb.exe`)
- run it from the main folder or it can't find the pictures
- it runs forever. press `Ctrl+C` to stop

## Folders

```
main.py         start here
adb/            finds devices, taps, swipes
automation/     device picker + auto jump
states/         every step of the bot (lobby, boost, in game, etc)
vision/         screenshots, picture matching, text reading
notification/   discord webhook stuff
config/         settings
tools/          adb
```

## Disclaimer

this is just a side project. it's not made by Devsisters or linked to them in any way. use it at your own risk.
