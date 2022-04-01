FROM python:slim-buster
WORKDIR /app
RUN apt-get update --fix-missing && apt-get install -y ffmpeg
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
