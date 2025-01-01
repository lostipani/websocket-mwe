FROM python:3.12-slim
RUN apt-get -y update; apt-get -y install curl

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY server/server.py /app

CMD ["python", "server.py"]