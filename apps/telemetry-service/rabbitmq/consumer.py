import pika
import json
import logging
from typing import Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            parameters = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            self.channel.queue_declare(queue=self.queue_name, durable=True)

            logger.info(f"Connected to RabbitMQ, queue: {self.queue_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            return False

    def consume(self, callback: Callable):

        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                logger.info(f"Received message: {message}")

                callback(message)

                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info("Message processed successfully")

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=on_message
        )

        logger.info("Waiting for messages...")
        self.channel.start_consuming()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Connection closed")
