FROM python:3.10

RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"

# Рабочая директория
WORKDIR /Todolist

# Установка зависимостей
COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Копирование файлов
COPY . .

# Запуск скрипта
ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

# Запуск приложения
#CMD ["gunicorn", "Todolist.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["gunicorn", "Todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]



## Новый конфиг
#FROM python:3.10
#
#RUN python -m venv /app/env
#ENV PATH="/app/env/bin:$PATH"
#
## Рабочая директория
#WORKDIR /Todolist
#
## Установка зависимостей
#COPY poetry.lock .
#COPY pyproject.toml .
#
#RUN pip install poetry \
#    && poetry config virtualenvs.create false \
#    && poetry install --no-root \
#
## Копирование файлов
#COPY . .
#
## Запуск скрипта
#ENTRYPOINT ["bash", "entrypoint.sh"]
#
## Открытие порта для входящих соединений
#EXPOSE 8000
#
## Запуск приложения
#CMD ["gunicorn", "Todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]