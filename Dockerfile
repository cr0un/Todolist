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
#    && poetry install --no-root
#
## Копирование файлов
#COPY . .
#
## Запуск приложения
#CMD ["gunicorn", "Todolist.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.10

RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"

# Рабочая директория
WORKDIR /Todolist

# Установка зависимостей
ADD poetry.lock .
ADD pyproject.toml .

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Копирование файлов
ADD . .

# Запуск приложения
CMD ["gunicorn", "Todolist.wsgi:application", "--bind", "0.0.0.0:8000"]

