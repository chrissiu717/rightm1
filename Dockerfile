FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver manually (v138)
RUN curl -sSL https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/138.0.7204.179/linux64/chromedriver-linux64.zip -o chromedriver.zip \
    && unzip chromedriver.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver.zip chromedriver-linux64

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]