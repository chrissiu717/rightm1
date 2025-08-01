FROM python:3.11-slim

# Install Chromium browser and the matching Chromium driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    unzip \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
