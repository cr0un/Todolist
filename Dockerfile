FROM python:3.10

RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"

# Рабочая директория
WORKDIR /Todolist

# Копирование файлов
COPY . .

# Установка зависимостей
#COPY poetry.lock .
#COPY pyproject.toml .
#
#RUN pip install poetry \
#    && poetry config virtualenvs.create false \
#    && poetry install --no-root

# Установите зависимости проекта
RUN pip install --no-cache-dir --use-pep517 -r requirements.txt

# Запуск приложения
CMD ["gunicorn", "Todolist.wsgi:application", "--bind", "0.0.0.0:8000"]

