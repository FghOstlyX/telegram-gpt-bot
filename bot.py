import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Хранение истории сообщений для каждого пользователя
user_conversations = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Напиши мне любой вопрос — и я отвечу через ИИ.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_input = update.message.text

    # Показываем индикатор "печатает"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Инициализация истории для пользователя, если её нет
    if user_id not in user_conversations:
        user_conversations[user_id] = [{"role": "system", "content": "Ты полезный и дружелюбный ИИ-помощник."}]

    # Добавляем сообщение пользователя в историю
    user_conversations[user_id].append({"role": "user", "content": user_input})

    try:
        # Запрос к OpenAI с учетом истории
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_conversations[user_id],
            max_tokens=500  # Ограничение на длину ответа
        )
        answer = response.choices[0].message.content

        # Добавляем ответ ИИ в историю
        user_conversations[user_id].append({"role": "assistant", "content": answer})

        # Ограничиваем длину истории (например, последние 10 сообщений)
        if len(user_conversations[user_id]) > 10:
            user_conversations[user_id] = user_conversations[user_id][-10:]

        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Произошла ошибка: {str(e)}. Попробуйте снова!")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация команд
    app.add_handler(CommandHandler("start", start))

    # Регистрация обработчика текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()