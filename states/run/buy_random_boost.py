import time

from adb.action import ClickAction, click, click_sequence
from vision.get_text import get_text
from vision.match_template import match_template
from vision.match_text import match_text
from vision.templates import BOOST, CHECK_BOX


def calculate_bounding_box(cx, cy):
    border_w = 380
    border_h = 50

    check_center_offset_x = 30
    check_center_offset_y = 30

    left = cx - check_center_offset_x
    top = cy - check_center_offset_y
    right = left + border_w
    bottom = top + border_h

    top_left = (left, top)
    bottom_right = (right, bottom)

    center = (
        (top_left[0] + bottom_right[0]) // 2,
        (top_left[1] + bottom_right[1]) // 2,
    )

    return top_left, bottom_right, center


def unselect_boosts(device_id, selected_random_boost):
    x, y = match_template(device_id, CHECK_BOX) or (0, 0)

    if not x or not y:
        return

    tl, br, box_center = calculate_bounding_box(x, y)

    _, _, text = match_text(device_id, selected_random_boost, tl, br) or (0, 0, "")

    if text not in selected_random_boost:
        click(
            device_id,
            (box_center[0] - 10, box_center[1] - 10),
            (box_center[0] + 10, box_center[1] + 10),
        )
        time.sleep(0.5)


def select_boosts(device_id, selected_random_boost):
    for boost in selected_random_boost:
        x, y, _ = match_text(device_id, [boost], (251, 151), (1014, 446)) or (0, 0, "")

        if not match_template(device_id, CHECK_BOX):
            click(device_id, (x - 10, y - 10), (x + 10, y + 10))
            time.sleep(0.5)


def check_current_boost(device_id, selected_random_boost):
    current_boost = get_text(device_id, (716, 519), (1077, 570))[0]
    current_boost = current_boost.lower().replace("~", "-")

    if current_boost in selected_random_boost:
        return current_boost

    return False


def buy_random_boost(device_id, bot, state_enum, config):
    selected_random_boost = config.get("Selected_Random_Boost", [])
    selected_random_boost = [boost.lower() for boost in selected_random_boost]
    buy_boost = config.get("Buy_Random_Boost", False)

    actions: list[ClickAction] = [
        ClickAction(
            tl=(486, 544),
            br=(583, 647),
            wait=0.5,
        ),
        ClickAction(
            tl=(1070, 178),
            br=(1120, 208),
            wait=0.5,
        ),
    ]

    if match_template(device_id, BOOST):
        if not check_current_boost(device_id, selected_random_boost):
            click_sequence(device_id, actions)

            unselect_boosts(device_id, selected_random_boost)
            select_boosts(device_id, selected_random_boost)

            click(device_id, (571, 576), (700, 599))

            while get_text(device_id, (720, 520), (1070, 560))[0].lower() not in selected_random_boost:
                time.sleep(1)

        return bot.update(device_id, state_enum.StartFromBoost)

    elif buy_boost:
        return bot.update(device_id, state_enum.BuyBoost)
    else:
        return bot.update(device_id, state_enum.StartFromLobby)
