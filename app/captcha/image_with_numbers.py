"""Numbers from image captcha resolver."""

import logging

from aiogram import types

from app.captcha import anti_captcha_provider
from app.captcha.symbol_traps_utils import replace_eng_chars

_common_pattern = 'отправьчислоскартинки'


async def image_with_numbers(message: str, message_object: types.Message) -> str | None:
    """Resolve image captcha by 3th-party service."""
    # todo impl for aiogram forward message with image
    if not message_object:
        return None

    question = replace_eng_chars(
        source=message.lower().replace(' ', ''),
    )
    if _common_pattern not in question:
        return None

    image_source = await get_photo_base64(message_object)
    if not image_source:
        logging.warning(f'captcha event - image not found! "{image_source}"')
        return None

    return await anti_captcha_provider.resolve_image_to_number(image_source)
