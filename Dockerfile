FROM python:3.10

RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"

# Рабочая директория
WORKDIR /Todolist

# Копирование файлов
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir --use-pep517 -r requirements.txt

# Запуск приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]