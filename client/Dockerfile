FROM python:3.12-slim

WORKDIR /app
COPY client/client.py /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "client.py"]