import time

from adb.action import ClickAction, click, click_sequence, swipe
from custom_types.types import Vector
from notification.discord_webhook import send_treasure_webhook
from utils.get_coins import get_coins
from utils.use_webhook import use_webhook
from vision.get_text import get_text
from vision.match_template import match_color, match_template
from vision.templates import CHOC_COOKIE, DISCONNECT, LOBBY, TREASURE

open_treasure_ui: list[ClickAction] = [
    ClickAction(
        tl=(1029, 531),
        br=(1137, 573),
        wait=1,
    ),
    ClickAction(
        tl=(245, 616),
        br=(382, 688),
        wait=1,
    ),
    ClickAction(
        tl=(178, 85),
        br=(285, 119),
        wait=1,
    ),
]


draw_treasure: list[ClickAction] = [
    ClickAction(
        tl=(255, 312),
        br=(349, 358),
        wait=1,
    ),
    ClickAction(
        tl=(602, 231),
        br=(641, 274),
        wait=2,
    ),
    ClickAction(
        tl=(554, 560),
        br=(730, 595),
        wait=0.2,
    ),
]

open_extract_ui: list[ClickAction] = [
    ClickAction(
        tl=(179, 86),
        br=(294, 123),
        wait=1,
    ),
    ClickAction(
        tl=(553, 668),
        br=(643, 700),
        wait=1,
    ),
    ClickAction(
        tl=(301, 80),
        br=(387, 113),
        wait=1,
    ),
    ClickAction(
        tl=(223, 321),
        br=(256, 343),
        wait=1,
    ),
]

extract_treasure: list[ClickAction] = [
    ClickAction(
        tl=(838, 654),
        br=(1014, 696),
        wait=0.5,
    ),
    ClickAction(
        tl=(556, 502),
        br=(723, 548),
        wait=2,
    ),
    ClickAction(
        tl=(556, 435),
        br=(733, 489),
        wait=1,
    ),
]


def is_disconnected(device_id):
    return match_template(device_id, DISCONNECT)


def swipe_up(device_id):
    for _ in range(2):
        swipe(device_id, (414, 530), (414, 250), 2000)
        time.sleep(0.25)


def check_choco_cookie(device_id, tl: Vector, br: Vector, config):

    keep_choc_cookie = config.get("Keep_Choc_Cookie", False)

    if not keep_choc_cookie:
        return False

    return (
        match_template(device_id, {"img": CHOC_COOKIE["img"], "tl": tl, "br": br})
        and keep_choc_cookie
    )


def auto_treasure(device_id, bot, state_enum, config):

    if not match_template(device_id, LOBBY):
        print(
            f"{device_id}: No lobby found, you must be in the lobby to use this function"
        )
        return bot.update(device_id, state_enum.Idle)

    print(f"{device_id}: Lobby found, starting treasure extraction...")

    attempt = 0
    total_magic_powder = 0
    current_magic_powder = 0
    coin_count = get_coins(device_id)

    print(f"{device_id}: Getting treasure inventory...")
    click_sequence(device_id, open_treasure_ui)
    time.sleep(1)

    raw_inv = (get_text(device_id, (934, 81), (1069, 112)) or ["0/0"])[0]
    # A misread here sets how many 5,000-coin draws to make: check it, cap by coins.
    current_inv, _, max_inv = raw_inv.replace(" ", "").partition("/")
    if not (current_inv.isdigit() and max_inv.isdigit()):
        raise ValueError(f"Couldn't read the treasure inventory: {raw_inv!r}")
    space_left = min(int(max_inv) - int(current_inv), coin_count // 5000)

    print(f"{device_id}: Data found, drawing treasure now")
    click(device_id, (1118, 88), (1138, 108))

    time.sleep(0.5)

    while match_template(device_id, TREASURE) and not is_disconnected(device_id):
        time.sleep(1)

        for _ in range(space_left):
            click_sequence(device_id, draw_treasure)
            coin_count -= 5000
        print(f"{device_id}: Draw completed, opening extract UI")

        click_sequence(device_id, open_extract_ui)
        print(f"{device_id}: Extract ui opened, starting treasure extraction")

        start_x = 210
        start_y = 191
        found_locked_treasure = False
        disconnected = False

        while not found_locked_treasure:
            for _ in range(4):
                for _ in range(4):
                    tl = (start_x - 70, start_y - 70)
                    br = (start_x + 70, start_y + 70)

                    if not check_choco_cookie(device_id, tl, br, config):
                        click(device_id, (start_x, start_y), (start_x, start_y))

                    start_x += 135

                    if match_color(device_id, (13, 40, 43), (717, 575)) or (
                        disconnected := is_disconnected(device_id)
                    ):
                        found_locked_treasure = True
                        time.sleep(3)

                        magic_powder = (
                            get_text(device_id, (983, 584), (1123, 612), True) or "0"
                        )[0].replace(",", "")
                        current_magic_powder = int(magic_powder)

                        break

                    time.sleep(0.25)

                if found_locked_treasure:
                    break

                start_x = 210
                start_y += 135

            if found_locked_treasure:
                break

            start_x = 210
            start_y = 191

            swipe_up(device_id)

        if disconnected:
            break

        time.sleep(2)

        click_sequence(device_id, extract_treasure)
        print(f"{device_id}: Extracted {current_magic_powder} magic powder")

        magic_powder = (get_text(device_id, (207, 678), (318, 703), True) or "0")[
            0
        ].replace(",", "")
        total_magic_powder = int(magic_powder)

        if use_webhook(config):
            send_treasure_webhook(
                {
                    "device_id": device_id,
                    "config": config,
                    "magic_powder": current_magic_powder,
                    "total_powder": total_magic_powder,
                    "current_coin": coin_count,
                }
            )

        click(device_id, (1118, 88), (1138, 108))

        current_magic_powder = 0
        attempt += 1
        print(f"{device_id}: Attempt {attempt} completed")

    print(f"{device_id}: Treasure ui not found, exiting...")
    return bot.update(device_id, state_enum.Idle)
