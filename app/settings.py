"""Application settings."""

import os

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings class."""

    available_gamebot_ids: set[int] = {776510403, 842830178}
    bot_token: str
    debug: bool = Field(default=False)
    anti_captcha_com_apikey: str = Field(default='', description='see https://anti-captcha.com for more information')
    anti_captcha_com_timeout: int = 15
    anti_captcha_com_create_task_tries: int = 3
    anti_captcha_com_create_task_throttling: int = 15
    anti_captcha_com_get_task_tries: int = 20
    anti_captcha_com_get_task_throttling: int = 5


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),  # type: ignore
)
