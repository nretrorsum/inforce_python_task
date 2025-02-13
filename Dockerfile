# Вибираємо базовий образ Python
FROM python:3.12-slim

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Оновлюємо систему та встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y git curl && apt-get clean

# Оновлюємо pip
RUN pip install --upgrade pip

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо та встановлюємо залежності Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . /app/

# Відкриваємо порт 8000
EXPOSE 8000

# Запускаємо міграції, збираємо статичні файли та запускаємо сервер
CMD ["bash", "-c", "python menuvote/manage.py migrate && python menuvote/manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 menuvote.wsgi:application"]

