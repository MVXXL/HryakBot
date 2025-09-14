<p align="light">
<h1 align="center">
 <a><img src="https://github.com/user-attachments/assets/a20cc4a5-c426-44e6-bc9c-5ffd24498a37" style="width: 25%;" alt="Hryak"></a>
 <h4 align="center">
 
  ![Python](https://img.shields.io/badge/Python-3.11%20%E2%80%94%203.12-blue)
  ![discord.py](https://img.shields.io/badge/discord.py-blue)
  ![LICENSE](https://img.shields.io/badge/license-CC_BY_NC_ND_4.0-green)
</h4>
</h1>


# HryakBot — исправленная, полностью рабочая версия

Это поддерживаемая и исправленная сборка популярного бота Hryak. Всё готово «из коробки»: достаточно заполнить `.env` и запустить.

Основные возможности:

- Кормите и прокачивайте своего хряка
- Переименовывайте и кастомизируйте внешность
- Добывайте и готовьте мясо, продавайте и зарабатывайте
- Покупайте буст-айтемы
- Сражайтесь в дуэлях и торгуйте с другими игроками

Что исправлено и улучшено:

- Перенос на SQLite по умолчанию (никакой MySQL не нужен) — база создаётся автоматически
- Исправлены ошибки UI-компонентов Discord (пустые Select-меню больше не ломают формы)
- Исправлены и усилены права и проверки команд (включая промокоды)
- Улучшена работа с изображениями и сетевыми сессиями

# ВАЖНО: ИЗОБРАЖЕНИЯ

В ЭТОМ РЕПОЗИТОРИИ НЕ ВСЕ КАРТИНКИ. ДЛЯ ПОЛНОЙ КОЛЛЕКЦИИ ИЗОБРАЖЕНИЙ СКАЧИВАЙТЕ ИХ ИЗ ОРИГИНАЛЬНОГО РЕПОЗИТОРИЯ:

https://github.com/Brevn0o/HryakBot

После загрузки поместите недостающие изображения в соответствующие папки `bin/images/` или используйте те пути, которые ожидает код.

# Gallery

You can see screenshots of the bot working below

<h1 align="center">
<a><img src="https://github.com/user-attachments/assets/d310045d-791c-430a-b2c4-ef61ff7d2659" style="width: 25%;" alt="Hryak"></a>
<a><img src="https://github.com/user-attachments/assets/04879545-9c94-4fd9-917a-a0364e64f408" style="width: 25%;" alt="Hryak"></a>
</h1>
<h1 align="center">
<a><img src="https://github.com/user-attachments/assets/08f1333f-c3f0-459d-a753-d9f53aa1a24a" style="width: 25%;" alt="Hryak"></a>
<a><img src="https://github.com/user-attachments/assets/472b8c84-1dd7-4fff-a14d-055c23f9a1d5" style="width: 25%;" alt="Hryak"></a>
<a><img src="https://github.com/user-attachments/assets/b3ed9007-4078-4fc4-b428-c395b981b3ac" style="width: 25%;" alt="Hryak"></a>
</h1>
<h1 align="center">
<a><img src="https://github.com/user-attachments/assets/a65f0690-3ed5-4395-9c25-9300f04415bd" style="width: 25%;" alt="Hryak"></a>
<a><img src="https://github.com/user-attachments/assets/697da951-ef15-463c-90e2-0c929da573b4" style="width: 25%;" alt="Hryak"></a>
<a><img src="https://github.com/user-attachments/assets/81195bd0-998e-43ff-97df-75f1405eb010" style="width: 25%;" alt="Hryak"></a>
</h1>

# Установка и запуск

Требования:

- Python 3.11–3.12
- Windows (рекомендовано), но работает и на других ОС

1) Установите зависимости

```
pip install -r requirements.txt
```

2) Заполните `.env` (минимум):

```
DISCORD_TOKEN=your_discord_bot_token
DB_ENGINE=sqlite
SQLITE_PATH=data/hryak.db
```

- По умолчанию используется SQLite. Файл базы создастся автоматически при первом запуске.
- Привилегированные интенты (Message Content) не обязательны для слэш-команд, но вы можете включить их в настройках приложения, если понадобятся.

3) Запуск

```
python main.py
```

или используйте `start.bat`.

После запуска бот подключится к Gateway, создаст базу и будет готов к работе.

