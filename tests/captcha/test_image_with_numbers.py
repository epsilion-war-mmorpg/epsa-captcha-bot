import uuid
from unittest.mock import Mock

from app.captcha.image_with_numbers import image_with_numbers

valid_captcha_message = '❓ На пути ты встретил капчу, отправь число с картинки или отправишься в тюрьму. У тебя есть 90 секунд'


async def test_image_with_numbers_happy_path(mocker):
    photo_object_mock = Mock()
    photo_object_mock.file_id = 'AgACAgIAAxkBAAMlZOPD3v3CD_88YzGxMJPZrrCLGKQAAinMMRsNaMlI2SZKGr-vdrIBAAMCAANzAAMwBA'
    photo_object_mock.file_unique_id = uuid.uuid4().hex
    message_mock = Mock()
    message_mock.photo = [photo_object_mock]
    anticaptcha_mocked = mocker.patch(
        'app.captcha.image_with_numbers.anti_captcha_provider.resolve_image_to_number',
        return_value='1234',
    )
    base64_getter_mocked = mocker.patch(
        'app.captcha.image_with_numbers.get_photo_base64',
        return_value='base64/sdsd/sd/sd',
    )

    result = await image_with_numbers(
        message=valid_captcha_message,
        message_object=message_mock,
    )

    assert base64_getter_mocked.call_count == 1
    assert anticaptcha_mocked.call_count == 1
    assert result == '1234'


async def test_image_with_numbers_have_no_media():
    message_mock = Mock()
    message_mock.photo = []

    result = await image_with_numbers(
        message=valid_captcha_message,
        message_object=message_mock,
    )

    assert result is None


async def test_image_with_numbers_skip_by_message():
    message_mock = Mock()
    message_mock.photo = ['sdsdsd']

    result = await image_with_numbers(
        message='сообщение из другой капчи',
        message_object=message_mock,
    )

    assert result is None


async def test_image_with_numbers_media_not_loaded(mocker):
    photo_object_mock = Mock()
    photo_object_mock.file_id = 'AgACAgIAAxkBAAMlZOPD3v3CD_88YzGxMJPZrrCLGKQAAinMMRsNaMlI2SZKGr-vdrIBAAMCAANzAAMwBA'
    photo_object_mock.file_unique_id = uuid.uuid4().hex
    message_mock = Mock()
    message_mock.photo = [photo_object_mock]
    base64_getter_mocked = mocker.patch(
        'app.captcha.image_with_numbers.get_photo_base64',
        return_value='',
    )

    result = await image_with_numbers(
        message=valid_captcha_message,
        message_object=message_mock,
    )

    assert result is None
    assert base64_getter_mocked.call_count == 1
