# SMM-система с ИИ

> Генерация контента, публикация в VK и Telegram, сбор базовой статистики в одном Python-проекте.

Проект автоматизирует типовой SMM-поток: создает текст и изображения через OpenAI, публикует результат в социальные сети и получает базовые метрики по опубликованным материалам.

## Быстрый старт

```bash
pip install -r requirements.txt
cp .env.example .env
python test_env.py
```

## Ключевые возможности

- **Генерация текста**: SMM-посты через OpenAI chat models.
- **Генерация изображений**: визуалы через DALL-E.
- **Публикация**: отправка в VK и Telegram.
- **Статистика**: сбор базовых метрик по постам.
- **Безопасность**: секреты через `.env`, без хранения токенов в репозитории.

## Пример

```python
from generators.text_gen import TextGenerator
from generators.image_gen import ImageGenerator

text = TextGenerator(tone="дружелюбный", topic="технологии", model="gpt-5").generate_post()
image = ImageGenerator(model="dall-e-3").generate_image("Современные технологии")

print(text)
print(image)
```

## Проверка запуска

```bash
python test.py
```

## Документация

| Руководство | Описание |
|-------------|----------|
| [Getting Started](docs/getting-started.md) | Установка, требования, первый запуск |
| [Configuration](docs/configuration.md) | Переменные окружения и настройки |
| [Architecture](docs/architecture.md) | Структура проекта и модули |
| [Testing](docs/testing.md) | Тесты и команды разработки |
| [Security](docs/security.md) | Практики безопасности и работа с секретами |

## Полезные файлы

- `test.py` — демонстрационный сценарий полного потока.
- `test_env.py` — проверка окружения и обязательных переменных.
- `run_tests.py` — запуск тестового набора.

## Лицензия

MIT License.
