from unittest.mock import AsyncMock

from app.bot import captcha


async def test_captcha_not_forward():
    message_mock = AsyncMock()
    message_mock.forward_from = None

    await captcha(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_captcha_forward_from_random_user_id():
    message_mock = AsyncMock()
    message_mock.forward_from.id = 123

    await captcha(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_captcha_forward_not_solved():
    message_mock = AsyncMock()
    message_mock.forward_from.id = 776510403
    message_mock.text = 'сообщение не про каптчу'

    await captcha(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_captcha_forward_happy_path():
    message_mock = AsyncMock()
    message_mock.forward_from.id = 776510403
    message_mock.text = 'На пути ты встретил капчу.\n 0 плюс десять - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд'

    await captcha(message=message_mock)

    message_mock.reply.assert_called_once()
