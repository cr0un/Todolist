FROM python:3.10

# Установка пакетного менеджера apt-get
RUN apt-get update && apt-get install -y vim

# Создание виртуального окружения внутри контейнера
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
CMD ["gunicorn", "Todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]