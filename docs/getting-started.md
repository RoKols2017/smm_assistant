[Back to README](../README.md) · [Configuration →](configuration.md)

# Getting Started

## Что понадобится

| Что | Зачем |
|-----|-------|
| Python 3.8+ | Запуск проекта |
| OpenAI API key | Генерация текста и изображений |
| VK token | Публикация и статистика VK |
| Telegram bot token | Публикация и статистика Telegram |

## Установка

```bash
pip install -r requirements.txt
```

## Настройка окружения

```bash
cp .env.example .env
python test_env.py
```

После копирования `.env.example` заполните реальные значения токенов и идентификаторов.

## Первый запуск

```bash
python test.py
```

Сценарий последовательно:

1. Генерирует текст поста.
2. Генерирует изображение.
3. Публикует результат в VK и Telegram.
4. Пытается собрать статистику по опубликованным материалам.

## Если нужен только модульный запуск

```bash
python generators/text_gen.py
python generators/image_gen.py
python social_publishers/vk_publisher.py
python social_publishers/telegram_publisher.py
python social_stats/stats_collector.py
```

## Что проверить при проблемах

- Заполнен ли `.env`.
- Доступны ли внешние API.
- Нет ли ошибок в `test_env.py`.
- Соответствуют ли токены нужным правам доступа.

## See Also

- [Configuration](configuration.md) — список переменных окружения и моделей.
- [Testing](testing.md) — как запускать тесты и проверки.
- [Security](security.md) — как безопасно хранить секреты.
