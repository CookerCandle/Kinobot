# Kinobot

Добро пожаловать в проект Kinobot! Этот README файл поможет вам установить и настроить репозиторий, а также объяснит дальнейшие действия.

## Установка

Следуйте этим шагам для установки репозитория:

1. Клонируйте репозиторий на ваш локальный компьютер:
    ```sh
    https://github.com/CookerCandle/Kinobot.git
    ```

2. Перейдите в директорию проекта:
    ```sh
    cd kinobot
    ```

3. Создайте виртуальное окружения и активируйте его:
    ```sh
    python -m venv .venv
    .venv/scripts/activate
    ```

4. Установите необходимые зависимости с помощью pip из файла `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

## Настройка

Перед запуском проекта, убедитесь, что у вас есть файл конфигурации. Создайте `.env` файл в корне проекта и заполните его, используя файл `.env.example` в качестве примера. Убедитесь, что все необходимые переменные окружения указаны корректно:

```
BOT_TOKEN=ваш_токен
ADMIN=[ваш_userid] -через запятую можно указать дополнительных админов
KINO_BASE=id_группы -создайте закрытую группу и добавьте бота в качестве админа

```

## Запуск

Для запуска проекта используйте следующую команду:

```sh
python main.py
```

## Вклад

Если вы хотите внести вклад в проект, пожалуйста, следуйте этим шагам:

1. Форкните репозиторий.
2. Создайте новую ветку (`git checkout -b feature-имя-фичи`).
3. Внесите изменения и закоммитьте их (`git commit -am 'Добавил новую фичу'`).
4. Запушьте изменения в ветку (`git push origin feature-имя-фичи`).
5. Создайте Pull Request.


Спасибо за использование Kinobot! Если не сложно оцените проект😊
