"""Numbers from image captcha resolver."""
import base64
import io
import logging

from aiogram import types

from app.bot_setup import bot
from app.captcha import anti_captcha_provider
from app.captcha.symbol_traps_utils import replace_eng_chars

_common_pattern = 'отправьчислоскартинки'


async def image_with_numbers(message: str, message_object: types.Message) -> str | None:
    """Resolve image captcha by 3th-party service."""
    question = replace_eng_chars(
        source=message.lower().replace(' ', ''),
    )
    if _common_pattern not in question or not message_object.photo:
        return None

    image_source = await get_photo_base64(message_object)
    if not image_source:
        logging.warning(f'captcha event - image not found! "{image_source}"')
        return None

    return await anti_captcha_provider.resolve_image_to_number(image_source)


async def get_photo_base64(message: types.Message) -> str:
    """Download and convert to base64 message photo."""
    file_content: io.BytesIO = await bot.download_file_by_id(message.photo[-1].file_id)
    image_str_base64 = base64.b64encode(file_content.getvalue()).decode('utf-8')
    return image_str_base64.replace('data:image/png;', '').replace('base64,', '')
