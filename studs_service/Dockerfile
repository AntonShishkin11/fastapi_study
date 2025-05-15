# Используем официальный Python образ как базовый
FROM python:3.11

# Устанавливаем системные зависимости, необходимые для работы с psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
ENV PYTHONPATH=/app

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app/

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порты для FastAPI
EXPOSE 8000

# Запускаем FastAPI с Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
