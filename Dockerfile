FROM python:3

ARG RABBITMQ_USER
ARG RABBITMQ_USER_PW
ARG RABBITMQ_DEV_HOST
ARG MONGODB_DEV_URI

ENV RABBITMQ_USER "$RABBITMQ_USER"
ENV RABBITMQ_USER_PW $RABBITMQ_USER_PW
ENV RABBITMQ_DEV_HOST "$RABBITMQ_DEV_HOST"
ENV MONGODB_DEV_URI "$MONGODB_DEV_URI"

WORKDIR scraper

COPY . .

RUN pip install -r requirements.txt

# The flag -u give unbuffered output, in order to see logs from python script
CMD ["python", "-u", "receive_barcode.py"]