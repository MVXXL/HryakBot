from ...core import *
from ..functions import Func, translate
from ..discord_utils import send_callback, generate_embed
from . import error_callbacks
from ..db_api import *


class Hidden:

    @staticmethod
    def get_user_tax_percent(user_id, currency: str, wealth: dict):
        if currency == 'coins':
            pchip_function = PchipInterpolator(np.array([0, 1000, 10000, 100000, 1000000000]),
                                               np.array([0, 5, 10, 15, 30]))
        elif currency == 'hollars':
            pchip_function = PchipInterpolator(np.array([0, 100, 1000, 10000, 1000000]),
                                               np.array([0, 5, 10, 15, 30]))
        else:
            pchip_function = PchipInterpolator(np.array([0, 1000000]),
                                               np.array([5, 5]))
        wealth = wealth[currency] if currency in wealth else 0
        tax = pchip_function(wealth)
        return round(float(tax), 1)

    @staticmethod
    @cached(TTLCache(maxsize=1000, ttl=86400))
    def remove_transparency(image_path):
        with Image.open(image_path) as img:
            bbox = img.getbbox()
            img = img.crop(bbox)
            img.save(image_path)
        return image_path





