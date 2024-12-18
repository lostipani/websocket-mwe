FROM python:3.12-slim

WORKDIR /app
COPY server/server.py /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r ./requirements.txt
EXPOSE 12345

CMD ["python", "server.py"]