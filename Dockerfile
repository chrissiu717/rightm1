FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    unzip \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver (v114)
RUN wget https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
