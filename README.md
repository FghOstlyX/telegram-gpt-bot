# Telegram GPT Bot

Telegram-бот с интеграцией OpenAI API. Подходит для автоматического ответа на вопросы.

## Установка:

1. Установи зависимости:
```bash
pip install -r requirements.txt
```

2. Создай .env файл:
```
TELEGRAM_BOT_TOKEN=ваш_токен
OPENAI_API_KEY=ваш_openai_ключ
```

3. Запусти:
```bash
python bot.py
```

## Команды:
- /start — приветствие
- /ask [вопрос] — получить ответ от ИИ
