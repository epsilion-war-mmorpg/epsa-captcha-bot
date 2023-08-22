"""Image captcha cache."""
from datetime import timedelta

from app.repo.connection import db_pool

CAPTCHA_FILE_KEY = 'captcha:image_file:{0}'


async def set_cached_answer(captcha_file_id: str, answer: str) -> None:
    """Save image captcha cache."""
    await db_pool.set(CAPTCHA_FILE_KEY.format(captcha_file_id), answer)
    await db_pool.expire(CAPTCHA_FILE_KEY.format(captcha_file_id), time=timedelta(days=7))


async def get_cached_answer(captcha_file_id: str) -> str | None:
    """Search cached captcha answer by file_id."""
    return await db_pool.get(CAPTCHA_FILE_KEY.format(captcha_file_id))
