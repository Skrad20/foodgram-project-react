FROM python:3.8.5
LABEL author='skrad200052@yandex.ru'  broken_keyboards=5pip
WORKDIR /code
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . .
CMD cd backend/; gunicorn --bind 0.0.0.0:8000 foodgram.wsgi