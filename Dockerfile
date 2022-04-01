FROM python:slim-buster
WORKDIR /app
RUN apt install ffmpeg
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
