



from aiogram import Router, Bot, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from lexicon import LEXICON
from config import Config, load_config
from aiogram import F
import logging
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.enums import ChatType
from service import validate_claim, save_claim



logger = logging.getLogger(__name__)
handlers = Router()
config : Config = load_config()


@handlers.message(F.photo, F.caption.startswith("#заявка"), F.chat.type == ChatType.GROUP)
async def correct_application_handler(message: Message):
    if message.caption is None:
        await message.reply("Добавьте подпись к фото с заявкой!")
        return

    photo_id = message.photo[-1].file_id  # самое большое фото
    text = message.caption
    isClaimed, restaurant, task_text, error_text = validate_claim(text)


    if isClaimed:
        await message.reply(f"""✅ Заявка из {restaurant.capitalize()} принята!
""")
    else:
        await message.reply(f"❌ {error_text}")
        return

    # Отправляем в Google Sheets
    result = await save_claim(restaurant=restaurant, task=task_text, file_id=photo_id)
    if result and result.get('success'):
        logger.info("✅ В таблицу добавлена новая заявка с фото")
    else:
        error_msg = result.get('error', 'Неизвестная ошибка') if result else 'Нет ответа'
        logger.error(f"❌ Ошибка при добавлении заявки в таблицу: {error_msg}")
        await message.reply("⚠️ Заявка принята, но возникла ошибка при сохранении в таблицу. Администратор уведомлён.")

    

@handlers.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def start_command_handler(message: Message):
    await message.answer(LEXICON["apply_only_in_group"])

@handlers.message(F.text.startswith("#заявка"), ~F.photo, F.chat.type == ChatType.GROUP)
async def incorrect_application_handler_no_photo(message: Message):
    await message.reply("Заявку можно отправить только с фотографией!")



