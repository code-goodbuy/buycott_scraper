FROM python:3

WORKDIR scraper

COPY . .

RUN pip install -r requirements.txt