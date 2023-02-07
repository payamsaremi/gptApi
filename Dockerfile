FROM python:3.9-slim

COPY ./src /app/src
COPY ./requirements.txt /app

COPY .env /app/.env

ENV $(cat /app/.env | xargs)

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--reload"]