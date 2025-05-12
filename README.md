# ChatGPT Telegram Bot

Многофункциональный Telegram-бот с поддержкой OpenAI GPT, генерации изображений, распознавания речи, Vision (анализ изображений), TTS (Text-to-Speech) и системой плагинов.

## Возможности
- Общение с ChatGPT (OpenAI GPT-3.5/4/4o и др.)
- Генерация изображений (DALL·E)
- Распознавание и синтез речи (Whisper, TTS)
- Интерпретация изображений (Vision)
- Работа с группами и приватными чатами
- Поддержка пользовательских и внешних плагинов (WolframAlpha, Spotify, погода, криптовалюты, поиск, перевод, и др.)
- Система лимитов и бюджетов пользователей
- Многоязычный интерфейс (через `translations.json`)
- Docker- и docker-compose-сборка

## Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd bot
```

### 2. Настройка переменных окружения
Создайте файл `.env` (пример уже есть в репозитории):
- `OPENAI_API_KEY` — ваш OpenAI API ключ
- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота от @BotFather
- Остальные параметры смотрите в `.env` и описании ниже

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск бота
```bash
python bot/main.py
```

### 5. Docker (опционально)
Для запуска через Docker:
```bash
docker-compose up --build
```

## Переменные окружения (основные)
- `OPENAI_API_KEY` — API-ключ OpenAI
- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота
- `OPENAI_MODEL` — используемая модель (например, gpt-4o, gpt-3.5-turbo и др.)
- `ENABLE_IMAGE_GENERATION` — включить генерацию изображений (true/false)
- `ENABLE_TTS_GENERATION` — включить синтез речи (true/false)
- `ENABLE_TRANSCRIPTION` — включить распознавание речи (true/false)
- `ENABLE_VISION` — включить Vision (анализ изображений)
- `ADMIN_USER_IDS` — ID админов через запятую
- `ALLOWED_TELEGRAM_USER_IDS` — разрешённые пользователи ("*" — все)
- `BOT_LANGUAGE` — язык бота (en, ru, и др.)
- `PLUGINS` — список включённых плагинов через запятую (см. ниже)
- См. также остальные переменные в `.env`

## Плагины
Список поддерживаемых плагинов (пример):
- `wolfram`, `weather`, `crypto`, `ddg_web_search`, `ddg_image_search`, `spotify`, `worldtimeapi`, `youtube_audio_extractor`, `dice`, `deepl_translate`, `gtts_text_to_speech`, `auto_tts`, `whois`, `webshot`, `iplocation`

Включайте нужные плагины через переменную `PLUGINS` в `.env`:
```
PLUGINS=wolfram,weather,crypto
```

## Команды бота
- `/help` — помощь
- `/reset` — сбросить диалог
- `/stats` — статистика использования
- `/resend` — повторить последний запрос
- `/image <prompt>` — сгенерировать изображение
- `/tts <текст>` — озвучить текст
- `/chat <сообщение>` — общение в группе

## Локализация
Для перевода интерфейса используйте файл `translations.json` и переменную `BOT_LANGUAGE`.

## Логи и статистика
- Логи использования и лимиты сохраняются в папке `usage_logs/`

## Обновление зависимостей
```bash
pip install -r requirements.txt --upgrade
```

## Docker
- `Dockerfile` и `docker-compose.yml` позволяют быстро развернуть бота в контейнере.
- Для работы TTS и аудио требуется ffmpeg (уже добавлен в Dockerfile).
