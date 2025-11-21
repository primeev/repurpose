FROM python:3.10

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV BOT_TOKEN="8508999864:AAHL1qmoQcNydfj3OrtvqXoSa-eZ9oksc3w"

CMD ["python", "main.py"]
