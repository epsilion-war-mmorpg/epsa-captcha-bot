"""Captcha resolve methods."""

from dataclasses import dataclass
from typing import Callable

from aiogram import types

from app.captcha.game_specific import game_specific
from app.captcha.image_with_numbers import image_with_numbers
from app.captcha.simple_emoji import simple_emoji
from app.captcha.simple_grammar import simple_grammar
from app.captcha.simple_math import simple_math
from app.settings import app_settings


@dataclass
class CaptchaAnswer:
    """Captcha answer type."""

    resolver_type: str
    question: str
    answer: str | None = None


async def try_resolve(message: types.Message) -> CaptchaAnswer:
    """Try to resolve captcha."""
    resolvers_enabled: list[Callable] = [
        game_specific,
        simple_math,
        simple_emoji,
        simple_grammar,
    ]

    if app_settings.anti_captcha_com_apikey:
        resolvers_enabled.append(image_with_numbers)

    for resolver in resolvers_enabled:
        answer_str = await resolver(message.text, message)
        if answer_str:
            return CaptchaAnswer(
                resolver_type=resolver.__name__,
                question=message.text,
                answer=answer_str,
            )

    return CaptchaAnswer(resolver_type='', question=message.text, answer=None)
