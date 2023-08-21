"""Telegram bot."""
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from app import custom_filters
from app.captcha.resolvers import try_resolve
from app.settings import app_settings

logger = logging.getLogger(__file__)

bot = Bot(
    token=app_settings.bot_token,
    parse_mode='Markdown',
)
router = Dispatcher(bot)


@router.message_handler(
    commands=['start', 'help'],
)
async def start(message: types.Message) -> None:
    """Show welcome message."""
    logger.info('start handler by {0}'.format(message.from_user.username))
    help_message = '\n'.join([
        'Бот помогает решать каптчу в игре Epsilion War.',
        'Просто перешлите сообщение с каптчей от игрового бота сюда.',
        '',
        'The bot helps to solve captchas in the game Epsilion War.',
        'Just forward the captcha message from the game bot here.',
    ])
    await message.reply(
        text=help_message,
        disable_web_page_preview=True,
    )


@router.message_handler(
    custom_filters.is_private,
    content_types=[types.ContentType.TEXT],
)
async def captcha(message: types.Message) -> None:
    """Try to solve captcha from forwarded message."""
    logger.info('captcha handler by {0}'.format(message.from_user.username))
    logger.info(message)
    # todo test

    if not message.forward_from or message.forward_from.id not in app_settings.available_gamebot_ids:
        await message.answer(
            text='\n'.join([
                'Перешлите сообщение от игрового бота! /help',
                'Forward the message from the game bot! /help',
            ])
        )
        return

    captcha_solve_response = await try_resolve(message)
    if not captcha_solve_response.answer:
        await message.answer(
            text='\n'.join([
                'Не смогли решить каптчу! =(',
                'Couldn`t solve the captcha! =(',
            ])
        )
        return

    await message.reply(
        text=captcha_solve_response.answer,
        disable_web_page_preview=True,
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )
    executor.start_polling(router, skip_updates=True)
