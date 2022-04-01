FROM python:3.11.0a6-alpine3.15
WORKDIR /app
RUN apk add -q --progress --update --no-cache ffmpeg
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
