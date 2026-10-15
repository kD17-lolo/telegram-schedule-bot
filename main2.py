import telebot
from telebot import types
from config import BOT_TOKEN
from database import (
    init_db,
    add_file,
    get_user_categories,
    search_files,
    set_user_state,
    get_user_state,
    clear_user_state,
)
bot = telebot.TeleBot(BOT_TOKEN)


#  Клавиатуры
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_search = types.KeyboardButton("🔍 Поиск по категории")
    btn_cats = types.KeyboardButton("📂 Мои категории")
    kb.add(btn_search, btn_cats)
    return kb


def cancel_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("❌ Отмена"))
    return kb


def generate_category_buttons(user_id):
    """Создаёт inline-клавиатуру с категориями пользователя"""
    kb = types.InlineKeyboardMarkup(row_width=2)
    categories = get_user_categories(user_id)
    for cat in categories:
        kb.add(types.InlineKeyboardButton(
            text=cat,
            callback_data=f"select_cat_{cat}"
        ))
    return kb


def pagination_keyboard(user_id, category, offset, total, limit=5):
    """Клавиатура для листания страниц"""
    kb = types.InlineKeyboardMarkup(row_width=3)
    buttons = []

    if offset > 0:
        buttons.append(types.InlineKeyboardButton(
            "⬅️ Назад",
            callback_data=f"page_{category}_{offset - limit}"
        ))

    buttons.append(types.InlineKeyboardButton(
        f"📄 {offset // limit + 1}/{(total + limit - 1) // limit}",
        callback_data="noop"
    ))

    if offset + limit < total:
        buttons.append(types.InlineKeyboardButton(
            "Вперёд ➡️",
            callback_data=f"page_{category}_{offset + limit}"
        ))

    kb.add(*buttons)
    kb.add(types.InlineKeyboardButton(
        "📋 Все категории",
        callback_data="back_to_cats"
    ))
    return kb


# Команды
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    clear_user_state(user_id)
    bot.send_message(
        user_id,
        "👋 Привет! Я бот-архив.\n\n"
        "📎 Отправь мне любой файл (фото, видео, документ), "
        "я спрошу категорию и сохраню его.\n\n"
        "🔍 Потом ты сможешь найти файлы по категориям.",
        reply_markup=main_keyboard()
    )


@bot.message_handler(commands=['search'])
def cmd_search(message):
    user_id = message.from_user.id
    categories = get_user_categories(user_id)

    if not categories:
        bot.send_message(user_id, "У тебя ещё нет сохранённых файлов. Отправь мне что-нибудь!")
        return

    kb = generate_category_buttons(user_id)
    bot.send_message(user_id, "📂 Выбери категорию для поиска:", reply_markup=kb)


#  Обработка текстовых команд
@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel(message):
    user_id = message.from_user.id
    clear_user_state(user_id)
    bot.send_message(user_id, "Действие отменено.", reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: m.text == "📂 Мои категории")
def list_categories(message):
    user_id = message.from_user.id
    categories = get_user_categories(user_id)

    if not categories:
        bot.send_message(user_id, "Пока нет ни одной категории. Отправь файл, чтобы создать первую!")
        return

    text = "📂 Твои категории:\n\n" + "\n".join(f"• {cat}" for cat in categories)
    kb = generate_category_buttons(user_id)
    bot.send_message(user_id, text, reply_markup=kb)


@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по категории")
def search_prompt(message):
    user_id = message.from_user.id
    categories = get_user_categories(user_id)

    if not categories:
        bot.send_message(user_id, "У тебя ещё нет файлов. Отправь что-нибудь!")
        return

    kb = generate_category_buttons(user_id)
    bot.send_message(user_id, "📂 Выбери категорию:", reply_markup=kb)


# Обработка ввода категории (когда пользователь печатает текст)
@bot.message_handler(func=lambda m: get_user_state(m.from_user.id) is not None)
def handle_category_input(message):
    user_id = message.from_user.id
    state = get_user_state(user_id)

    if state and state["state"] == "waiting_category":
        category = message.text.strip()
        if not category:
            bot.send_message(user_id, "Название категории не может быть пустым. Попробуй ещё раз:",
                             reply_markup=cancel_keyboard())
            return

        # Сохраняем файл
        add_file(
            user_id=user_id,
            file_id=state["temp_file_id"],
            file_type=state["temp_file_type"],
            file_name=state["temp_file_name"],
            category=category
        )

        clear_user_state(user_id)

        bot.send_message(
            user_id,
            f"✅ Файл сохранён в категорию «{category}»!",
            reply_markup=main_keyboard()
        )


#  Обработка файлов (фото, видео, документы)
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'voice'])
def handle_file(message):
    user_id = message.from_user.id
    file_type = message.content_type

    # Определяем file_id и имя файла
    if file_type == 'photo':
        file_id = message.photo[-1].file_id  # берём самое большое разрешение
        file_name = "photo.jpg"
    elif file_type == 'video':
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"
    elif file_type == 'document':
        file_id = message.document.file_id
        file_name = message.document.file_name or "document"
    elif file_type == 'audio':
        file_id = message.audio.file_id
        file_name = message.audio.title or "audio"
    elif file_type == 'voice':
        file_id = message.voice.file_id
        file_name = "voice_message"
    else:
        return

    # Сохраняем временные данные
    set_user_state(
        user_id=user_id,
        state="waiting_category",
        temp_file_id=file_id,
        temp_file_type=file_type,
        temp_file_name=file_name
    )

    # Показываем существующие категории + предлагаем ввести новую
    categories = get_user_categories(user_id)

    text = f"📎 Файл получен: *{file_name}*\n\n📂 В какую категорию сохранить?"

    if categories:
        text += "\n_Выбери из списка или введи новое название:_"
        kb = generate_category_buttons(user_id)
        # Добавляем кнопку для ввода новой категории
        kb.add(types.InlineKeyboardButton("✏️ Ввести новую", callback_data="new_category"))
    else:
        text += "\n_Введи название новой категории:_"
        kb = None  # пользователь введёт текст

    if kb:
        bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=kb)
    else:
        bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=cancel_keyboard())


# === Обработка inline-кнопок ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    data = call.data

    # Выбор существующей категории (при сохранении файла)
    if data.startswith("select_cat_"):
        category = data.replace("select_cat_", "")
        state = get_user_state(user_id)

        if state and state["state"] == "waiting_category":
            # Сохраняем файл в выбранную категорию
            add_file(
                user_id=user_id,
                file_id=state["temp_file_id"],
                file_type=state["temp_file_type"],
                file_name=state["temp_file_name"],
                category=category
            )
            clear_user_state(user_id)
            bot.edit_message_text(
                f"✅ Файл сохранён в категорию «{category}»!",
                user_id,
                call.message.message_id
            )
        else:
            # Это поиск — показываем файлы категории
            show_category_files(user_id, category, offset=0, edit_msg_id=call.message.message_id)

        bot.answer_callback_query(call.id)

    # Кнопка "Ввести новую категорию"
    elif data == "new_category":
        bot.edit_message_text(
            "✏️ Введи название новой категории:",
            user_id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)

    # Пагинация
    elif data.startswith("page_"):
        parts = data.split("_")
        category = "_".join(parts[1:-1])  # на случай если категория содержит "_"
        offset = int(parts[-1])
        show_category_files(user_id, category, offset=offset, edit_msg_id=call.message.message_id)
        bot.answer_callback_query(call.id)

    # Назад к списку категорий
    elif data == "back_to_cats":
        kb = generate_category_buttons(user_id)
        try:
            bot.edit_message_text("📂 Выбери категорию:", user_id, call.message.message_id, reply_markup=kb)
        except:
            pass
        bot.answer_callback_query(call.id)

    # Заглушка для неактивных кнопок
    elif data == "noop":
        bot.answer_callback_query(call.id)


def show_category_files(user_id, category, offset=0, edit_msg_id=None):
    """Отображает файлы категории с пагинацией"""
    files, total = search_files(user_id, category, offset=offset, limit=5)

    if total == 0:
        text = f"📂 В категории «{category}» ничего не найдено."
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📋 Все категории", callback_data="back_to_cats"))

        if edit_msg_id:
            bot.edit_message_text(text, user_id, edit_msg_id, reply_markup=kb)
        else:
            bot.send_message(user_id, text, reply_markup=kb)
        return

    # Отправляем файлы
    text = f"📂 Категория «{category}» ({total} файлов):\n"

    if edit_msg_id:
        # Сначала шлём файлы
        for f in files:
            try:
                if f["file_type"] == "photo":
                    bot.send_photo(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "video":
                    bot.send_video(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "document":
                    bot.send_document(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "audio":
                    bot.send_audio(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "voice":
                    bot.send_voice(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
            except Exception as e:
                bot.send_message(user_id, f"⚠️ Не удалось отправить файл: {e}")

        # Обновляем сообщение с информацией
        kb = pagination_keyboard(user_id, category, offset, total)
        try:
            bot.edit_message_text(text, user_id, edit_msg_id, reply_markup=kb)
        except:
            bot.send_message(user_id, text, reply_markup=kb)
    else:
        for f in files:
            try:
                if f["file_type"] == "photo":
                    bot.send_photo(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "video":
                    bot.send_video(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "document":
                    bot.send_document(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "audio":
                    bot.send_audio(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
                elif f["file_type"] == "voice":
                    bot.send_voice(user_id, f["file_id"], caption=f"📎 {f['file_name']}")
            except Exception as e:
                bot.send_message(user_id, f"⚠️ Не удалось отправить файл: {e}")

        kb = pagination_keyboard(user_id, category, offset, total)
        bot.send_message(user_id, text, reply_markup=kb)


# === Запуск ===
if __name__ == "__main__":
    init_db()
    print("✅ Бот запущен!")
    bot.infinity_polling()