FROM python:3.13-slim-bullseye

WORKDIR /msgpack_django

COPY . /msgpack_django/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["./run_granian.sh"]
