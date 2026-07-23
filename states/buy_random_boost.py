import time

from vision.template_match import match_template, match_color
from adb.action import click_sequence, ClickAction, click
from vision.templates import BOOST, CHECK_BOX
from config.config import load_config
from vision.text_match import match_text


def buy_random_boost(bot, state_enum):

    config = load_config()
    selected_random_boost = config.get('Selected_Random_Boost', [])
    buy_boost = config.get('Buy_Random_Boost', False)

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

    def calculate_bounding_box(cx, cy):
        half_w = 380 // 2
        half_h = 50 // 2

        top_left = (cx - half_w, cy - half_h)
        bottom_right = (cx + half_w, cy + half_h)

        center = (
            (top_left[0] + bottom_right[0]) // 2,
            (top_left[1] + bottom_right[1]) // 2,
        )

        return top_left, bottom_right, center

    def unselect_boosts(selected_random_boost):
        x, y = match_template(CHECK_BOX["img"], CHECK_BOX["tl"], CHECK_BOX["br"]) or (0,0)

        if not x or not y:
            return

        tl, br, box_center = calculate_bounding_box(x, y)

        _, _, text = match_text(selected_random_boost, tl, br) or (0, 0, "")

        if text not in selected_random_boost:
            print(f"unselecting {text} and user selected {selected_random_boost}")
            click((box_center[0] - 10, box_center[1] - 10), (box_center[0] + 10, box_center[1] + 10))
            time.sleep(0.5)

    def select_boosts(selected_random_boost):
        for boost in selected_random_boost:
            x, y, _ = match_text([boost], (251, 151), (1014, 446)) or (0,0, "")

            if not match_template(CHECK_BOX["img"], CHECK_BOX["tl"], CHECK_BOX["br"]):
                click((x - 10, y - 10), (x + 10, y + 10))
                time.sleep(0.5)

    if match_template(BOOST["img"], BOOST["tl"], BOOST["br"]) and bot.state == state_enum.RandomBoost:

        click_sequence(actions)

        unselect_boosts(selected_random_boost)
        select_boosts(selected_random_boost)

        click((571, 576), (700, 599))

        while match_color((78, 77, 75), (140, 330)):
           time.sleep(1)

        return bot.update(state_enum.StartFromBoost)
    elif buy_boost:
        return bot.update(state_enum.BuyBoost)
    else:
        return bot.update(state_enum.StartFromLobby)
