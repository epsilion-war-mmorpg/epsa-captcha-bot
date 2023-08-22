"""Numbers from image captcha resolver."""
import base64
import io
import logging

from aiogram import types

from app.bot_setup import bot
from app.captcha import anti_captcha_provider
from app.captcha.symbol_traps_utils import replace_eng_chars
from app.repo.captcha_cache import get_cached_answer, set_cached_answer

_common_pattern = 'отправьчислоскартинки'


async def image_with_numbers(message: str, message_object: types.Message) -> str | None:
    """Resolve image captcha by 3th-party service."""
    question = replace_eng_chars(
        source=message.lower().replace(' ', ''),
    )
    if _common_pattern not in question or not message_object.photo:
        return None

    cache_key = message_object.photo[-1].file_unique_id
    cached_answer = await get_cached_answer(cache_key)
    if cached_answer:
        return cached_answer

    image_source = await get_photo_base64(message_object.photo[-1].file_id)
    if not image_source:
        logging.warning(f'captcha event - image not found! "{image_source}"')
        return None

    answer = await anti_captcha_provider.resolve_image_to_number(image_source)
    if answer:
        await set_cached_answer(cache_key, answer)

    return answer


async def get_photo_base64(file_id: str) -> str:
    """Download and convert to base64 message photo."""
    file_content: io.BytesIO = await bot.download_file_by_id(file_id)
    image_str_base64 = base64.b64encode(file_content.getvalue()).decode('utf-8')
    return image_str_base64.replace('data:image/png;', '').replace('base64,', '')
