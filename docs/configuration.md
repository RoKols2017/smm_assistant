[← Getting Started](getting-started.md) · [Back to README](../README.md) · [Architecture →](architecture.md)

# Configuration

## Файл `.env`

Проект ожидает конфигурацию через переменные окружения. Для локальной разработки используйте `.env`, созданный из `.env.example`.

## Обязательные переменные

| Переменная | Назначение |
|------------|------------|
| `OPENAI_API_KEY` | Ключ OpenAI для генерации текста и изображений |
| `VK_TOKEN` | Токен VK API |
| `VK_GROUP_ID` | Идентификатор группы VK |
| `TG_TOKEN` | Токен Telegram-бота |
| `TG_CHAT_ID` | Идентификатор Telegram-чата или канала |

## Дополнительные переменные

| Переменная | Назначение | Значение из README |
|------------|------------|--------------------|
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `MAX_RETRIES` | Количество повторов для операций | `3` |
| `TIMEOUT` | Таймаут внешних запросов | `30` |
| `OPENAI_TEXT_MODEL` | Модель для текста | `gpt-5` |
| `OPENAI_IMAGE_MODEL` | Модель для изображений | `dall-e-3` |

## Пример

```bash
OPENAI_API_KEY=your_openai_key_here
VK_TOKEN=your_vk_token_here
VK_GROUP_ID=your_vk_group_id_here
TG_TOKEN=your_telegram_token_here
TG_CHAT_ID=your_telegram_chat_id_here
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT=30
OPENAI_TEXT_MODEL=gpt-5
OPENAI_IMAGE_MODEL=dall-e-3
```

## Практические замечания

- Не коммитьте `.env` в репозиторий.
- Для production лучше задавать переменные через окружение, а не через файл.
- Перед первым запуском всегда прогоняйте `python test_env.py`.

## See Also

- [Getting Started](getting-started.md) — начальная настройка проекта.
- [Security](security.md) — правила работы с токенами и секретами.
- [Architecture](architecture.md) — где используются интеграции и модули.
