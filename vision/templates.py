from typing import TypedDict

from custom_types.types import Vector


class TemplateType(TypedDict):
    img: str
    tl: Vector
    br: Vector


LOBBY: TemplateType = {
    "img": "lobby",
    "tl": (740, 500),
    "br": (1170, 600),
}
X_POPUP: TemplateType = {
    "img": "x_popup",
    "tl": (850, 0),
    "br": (1280, 180),
}
GET_RELIC: TemplateType = {
    "img": "get_relic",
    "tl": (479, 61),
    "br": (579, 108),
}
BOOST: TemplateType = {
    "img": "boost",
    "tl": (110, 68),
    "br": (632, 149),
}
CHECK_BOX: TemplateType = {
    "img": "check_box",
    "tl": (251, 151),
    "br": (1014, 446),
}
START_GAME: TemplateType = {
    "img": "play",
    "tl": (665, 550),
    "br": (1121, 660),
}
IN_GAME: TemplateType = {
    "img": "in_game",
    "tl": (1160, 0),
    "br": (1238, 72),
}
FAST_START: TemplateType = {
    "img": "fast_start",
    "tl": (565, 257),
    "br": (744, 428),
}
COOKIE_RELAY: TemplateType = {
    "img": "cookie_relay",
    "tl": (565, 257),
    "br": (744, 428),
}
MATCH_END: TemplateType = {
    "img": "end_match",
    "tl": (295, 567),
    "br": (635, 675),
}
OPEN_BOX: TemplateType = {
    "img": "open_box",
    "tl": (474, 586),
    "br": (793, 699),
}
TREASURE: TemplateType = {
    "img": "treasure",
    "tl": (193, 293),
    "br": (384, 364),
}
DISCONNECT: TemplateType = {
    "img": "disconnect",
    "tl": (281, 152),
    "br": (1000, 568),
}
SEND_LIVES: TemplateType = {
    "img": "send_lives",
    "tl": (131, 229),
    "br": (1153, 490),
}
CLAIM_LIVES: TemplateType = {
    "img": "claim_lives",
    "tl": (131, 229),
    "br": (1153, 490),
}
CHOC_COOKIE: TemplateType = {
    "img": "choc_cookie",
    "tl": (0, 0),
    "br": (0, 0),
}
