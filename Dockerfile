# Базовий імідж
FROM python:3.10-slim

# Встановлюємо залежності
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Встановлюємо Chromium та ChromeDriver для Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо весь код в контейнер
COPY . .

# Запускаємо FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
