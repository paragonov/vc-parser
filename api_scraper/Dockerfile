FROM python:3.9.6-alpine

WORKDIR /api_scraper/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /api_scraper/entrypoint.sh
RUN chmod +x /api_scraper/entrypoint.sh

COPY . .

ENTRYPOINT ["/api_scraper/entrypoint.sh"]