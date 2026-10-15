from telebot import types

# Структура: специальность -> группы
SCHEDULE_DATA = {
    "Инб": [
        "ИНБ-б-о-23-1", "ИНБ-б-о-23-2", "ИНБ-б-о-23-3",
        "ИНБ-б-о-24-1", "ИНБ-б-о-24-2", "ИНБ-б-о-25-1", "ИНБ-б-о-25-2",
    ],
    "Ибас": [
        "ИБАС-с-о-23-1",
        "ИБАС-с-о-23-2", "ИБАС-с-о-24-1", "ИБАС-с-о-25-1"
    ],
    "Ибтс": [
        "ИБТС-с-о-23-2", "ИБТС-с-о-24-1"
    ],
    "Кмб": [
        "КМБ-с-о-23-1", "КМБ-с-о-24-1", "КМБ-с-о-25-1"
    ],
    "Мкн": [
        "МКН-б-о-23-1", "МКН-б-о-23-2",
        "МКН-б-о-24-1", "МКН-б-о-24-2", "МКН-б-о-25-1", "МКН-б-о-25-2",
        "МКН-м-о-24-1", "МКН-м-о-25-1"
    ],
    "Под": [
        "ПОБ-м-о-24-2", "ПОБ-м-о-24-8", "ПОБ-м-о-25-1", "ПОБ-м-о-25-2"
    ],
    "Под2": [
        "ПОД-б-о-23-1", "ПОД-б-о-23-6", "ПОД-б-о-23-7",
        "ПОД-б-о-24-1", "ПОД-б-о-24-2", "ПОД-б-о-24-7",
        "ПОД-б-о-24-8", "ПОД-б-о-25-3"
    ],
    "Пми": [
        "ПМИ-б-о-23-1", "ПМИ-б-о-23-2",
        "ПМИ-б-о-24-1", "ПМИ-б-о-24-2", "ПМИ-б-о-25-1",
        "ПМИ-б-о-25-2", "ПМИ-м-о-22-1", "ПМИ-м-о-23-1",
        "ПМИ-м-о-24-1", "ПМИ-м-о-25-1"
    ]
}

# Ссылки на расписание (замените на реальные!)
SCHEDULE_LINKS = {
    "ИНБ-б-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18173",
    "ИНБ-б-о-23-2":"https://ecampus.ncfu.ru/schedule/group/18241",
    "ИНБ-б-о-23-3":"https://ecampus.ncfu.ru/schedule/group/18604",
    "ИНБ-б-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18735",
    "ИНБ-б-о-24-2":"https://ecampus.ncfu.ru/schedule/group/18736",
    "ИНБ-б-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19396",
    "ИНБ-б-о-25-2":"https://ecampus.ncfu.ru/schedule/group/19397",
    "ИБАС-с-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18225",
    "ИБАС-с-о-23-2":"https://ecampus.ncfu.ru/schedule/group/18263",
    "ИБАС-с-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18811",
    "ИБАС-с-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19402",
    "ИБТС-с-о-23-2":"https://ecampus.ncfu.ru/schedule/group/19743",
    "ИБТС-с-о-24-1":"https://ecampus.ncfu.ru/schedule/group/19758",
    "КМБ-с-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18224",
    "КМБ-с-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18810",
    "КМБ-с-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19401",
    "МКН-б-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18157",
    "МКН-б-о-23-2":"https://ecampus.ncfu.ru/schedule/group/18158",
    "МКН-б-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18706",
    "МКН-б-о-24-2":"https://ecampus.ncfu.ru/schedule/group/18707",
    "МКН-б-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19394",
    "МКН-б-о-25-2":"https://ecampus.ncfu.ru/schedule/group/19395",
    "МКН-м-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18837",
    "МКН-м-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19343",
    "ПОБ-м-о-24-2":"https://ecampus.ncfu.ru/schedule/group/18916",
    "ПОБ-м-о-24-8":"https://ecampus.ncfu.ru/schedule/group/18924",
    "ПОБ-м-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19403",
    "ПОБ-м-о-25-2":"https://ecampus.ncfu.ru/schedule/group/19404",
    "ПОД-б-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18213",
    "ПОД-б-о-23-6":"https://ecampus.ncfu.ru/schedule/group/18284",
    "ПОД-б-о-23-7":"https://ecampus.ncfu.ru/schedule/group/18635",
    "ПОД-б-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18794",
    "ПОД-б-о-24-2":"https://ecampus.ncfu.ru/schedule/group/18795",
    "ПОД-б-о-24-7":"https://ecampus.ncfu.ru/schedule/group/19128",
    "ПОД-б-о-24-8":"https://ecampus.ncfu.ru/schedule/group/19131",
    "ПОД-б-о-25-3":"https://ecampus.ncfu.ru/schedule/group/19391",
    "ПМИ-б-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18155",
    "ПМИ-б-о-23-2":"https://ecampus.ncfu.ru/schedule/group/18156",
    "ПМИ-б-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18704",
    "ПМИ-б-о-24-2":"https://ecampus.ncfu.ru/schedule/group/18705",
    "ПМИ-б-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19392",
    "ПМИ-б-о-25-2":"https://ecampus.ncfu.ru/schedule/group/19393",
    "ПМИ-м-о-22-1":"https://ecampus.ncfu.ru/schedule/group/16707",
    "ПМИ-м-о-23-1":"https://ecampus.ncfu.ru/schedule/group/18285",
    "ПМИ-м-о-24-1":"https://ecampus.ncfu.ru/schedule/group/18984",
    "ПМИ-м-о-25-1":"https://ecampus.ncfu.ru/schedule/group/19342"
    }

# Запасная ссылка для групп без индивидуальной
DEFAULT_SCHEDULE_LINK = "https://ecampus.ncfu.ru/schedule"


def get_specialties_keyboard():
    """Клавиатура выбора специальности"""
    kb = types.InlineKeyboardMarkup(row_width=1)
    for spec in SCHEDULE_DATA.keys():
        kb.add(types.InlineKeyboardButton(
            text=spec,
            callback_data=f"spec_{spec}"
        ))
    return kb


def get_groups_keyboard(specialty):
    """Клавиатура выбора группы"""
    kb = types.InlineKeyboardMarkup(row_width=3)
    groups = SCHEDULE_DATA.get(specialty, [])
    for group in groups:
        kb.add(types.InlineKeyboardButton(
            text=group,
            callback_data=f"group_{group}"
        ))
    kb.add(types.InlineKeyboardButton(
        "🔙 Назад к специальностям",
        callback_data="back_to_specialties"
    ))
    return kb


def get_schedule_link(group):
    """Возвращает ссылку на расписание группы"""
    return SCHEDULE_LINKS.get(group, DEFAULT_SCHEDULE_LINK)