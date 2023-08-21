from unittest.mock import AsyncMock

from app.bot import captcha


async def test_captcha():
    message_mock = AsyncMock()
    message_mock.forward_from = None
    message_mock.contact = None
    message_mock.text = ''

    await captcha(message=message_mock)

    message_mock.answer.assert_called_once()
