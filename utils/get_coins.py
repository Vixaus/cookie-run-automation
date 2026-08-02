from vision.get_text import get_text


def get_coins(device_id):
    coin_text = (get_text(device_id, (551, 21), (683, 53), True))[0]
    coin_int = int(coin_text.replace(",", ""))
    return coin_int
