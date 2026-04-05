[← Architecture](architecture.md) · [Back to README](../README.md) · [Security →](security.md)

# Testing

## Базовые проверки

Проверка окружения:

```bash
python test_env.py
```

Полный демонстрационный прогон:

```bash
python test.py
```

## Запуск тестов

Через helper-скрипт:

```bash
python run_tests.py
```

Напрямую через `pytest`:

```bash
python -m pytest tests/ --cov=. --cov-report=html --cov-fail-under=80
```

## Что покрыто

- генерация текста;
- генерация изображений;
- VK publisher;
- Telegram publisher;
- сбор статистики;
- интеграционный сценарий.

## Команды разработки

```bash
pip install -r requirements.txt
pip install -e .
flake8 .
black .
```

## Практика использования

- Перед изменениями конфигурации запускайте `test_env.py`.
- Перед изменениями модулей прогоняйте релевантные тесты из `tests/`.
- Перед крупными изменениями полезно запускать полный `pytest` с покрытием.

## See Also

- [Getting Started](getting-started.md) — установка и первый запуск.
- [Architecture](architecture.md) — какие модули покрываются тестами.
- [Security](security.md) — что не должно попадать в логи и фикстуры.
