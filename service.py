import re
import aiohttp
import asyncio
from datetime import datetime
from config import Config, load_config
import logging

config: Config = load_config()
logger = logging.getLogger(__name__)

def validate_claim(text: str) -> tuple[bool, str, str, str]:

    allowed_restaurants: set = {"ДУО", "ТАРТАР", "АЗИЯ", "ХАРВЕСТ", "РЕКОЛЬТЕ", "ФРАНЦУЗ", "ОДЖИ", "ПЕРЕМЕНА"}
    """
    Проверяет, соответствует ли текст заявки требуемому формату.
    
    Аргументы:
        text: строка с текстом заявки.
        allowed_restaurants: множество допустимых названий ресторанов.
    
    Возвращает:
        Кортеж (is_valid, restaurant, task, error_message):
            is_valid: bool – успешна ли проверка.
            restaurant: str – извлечённое название ресторана (пустая строка при ошибке).
            task: str – извлечённый текст задачи (пустая строка при ошибке).
            error_message: str – описание ошибки (пустая строка, если is_valid=True).
    """
    # Регулярное выражение: #заявка, затем пробелы, (название), пробелы, текст задачи
    pattern = r'^#заявка\s+\(([^)]+)\)\s*(.*)$'
    match = re.match(pattern, text.strip())
    
    if not match:
        return False, "", "", "Неверный формат. Должно быть: #заявка (НАЗВАНИЕ) текст задачи"
    
    restaurant = match.group(1).strip()
    task = match.group(2).strip()
    
    if not restaurant:
        return False, "", "", "Название ресторана не может быть пустым"
    
    if restaurant not in allowed_restaurants:
        return False, "", "", f"Ресторан '{restaurant}' не найден в списке допустимых"
    
    if not task:
        return False, "", "", "Текст задачи не может быть пустым"
    
    return True, restaurant, task, ""


async def save_claim(restaurant: str, task: str, file_id: str):
    url = "https://script.google.com/macros/s/AKfycbytdCFJm6wU9Py4CqM7yJdp7tt5nmRz7aDTUFUcbvBYxeP1_gYD3nbKE035gzcFQPeP/exec"
    current_datetime = datetime.now().strftime("%d/%m/%Y")

    payload = {
        "restaurant": restaurant,
        "task": task,
        "date": current_datetime,
        "photo_file_id": file_id,
        "bot_token": config.bot.token
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            logger.info(f"📬 Ответ от Apps Script: {result}")
            return result