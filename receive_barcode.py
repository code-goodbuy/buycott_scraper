#!/usr/bin/env python3
import pika, sys, os, json, pymongo
from buycott_scraper import BuycottScraper


def main():
    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_USER_PW'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_DEV_HOST'),
        port=os.getenv('RABBITMQ_PORT'),
        credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='buycott', durable=True)

    def connect_db():
        client = pymongo.MongoClient(
            os.environ['MONGODB_DEV_URI'])
        db = client.dev
        return db

    def save_product(db, product):
        db["products"].insert_one(product)
        print(" [+] Product successfully saved.")

    def callback(ch, method, properties, code):
        print(f" [!] Received {code} \n Starting Scraper... ")
        scraper = BuycottScraper(code)
        product = scraper.scrape()
        print("Scraped New Product:\n", json.dumps(product, indent=4, sort_keys=True))
        try:
            db = connect_db()
            save_product(db, product)
        except Exception as e:
            print(f"Error while saving product {str(e)}")
        print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue='buycott', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
