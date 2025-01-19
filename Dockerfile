FROM debian:12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip chromium chromium-driver && rm -rf /var/lib/apt/lists/*
    
COPY . .

RUN pip install -r requirements.txt --break-system-packages

CMD ["python3", "main.py"]