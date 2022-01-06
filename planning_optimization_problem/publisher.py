"""
File Name: publisher.py
* Django App Name: planning_optimization_problem
* Description:
  This file includes the class definition of a RabbitMQ message publisher.
"""

import pika
import json
import logging
from planning_optimization_problem.settings import (RABBITMQ_HOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD, host=RABBITMQ_HOST):
        """
        * Method Name: __init__
        * Description: This method is used to initialize the RabbitMQ publisher.
        * Parameters:
            - username: str
            - password: str
            - host: str
        """
        self.username = username
        self.password = password
        self.host = host
        self.channel = None
        self.queue = None

    def _init_channel(self):
        """
        * Method Name: _init_channel
        * Description: This method is used to establish a connection to the RabbitMQ and create a channel.
        :return: The channel object
        """
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = connection.channel()
        return self.channel

    def _init_queue(self, queue_name, exchange_name, routing_key):
        """
        * Method Name: _init_queue
        * Description: This method is used to declare exchange and queue and then bind the queue to the exchange using
        a routing_key and the predefined channel.
        * Parameters:
            - queue_name: str
            - exchange_name: str
            - routing_key: str
        :return: The queue object
        """
        self.channel.exchange_declare(exchange=exchange_name, durable=True, exchange_type="topic")
        queue = self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        self.queue = queue_name
        return queue.method.queue

    def publish(self, queue_name, exchange_name, routing_key, message):
        """
        * Method Name: publish
        * Description: This method creates the channel and queue (if they are not created or closed) and starts to publish
        messages to that queue using a routing_key and the predefined channel.
        * Parameters:
            - queue_name: str
            - exchange_name: str
            - routing_key: str
            - message: dict
        """
        if self.channel is None:
            self._init_channel()
        if self.queue is None:
            self._init_queue(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)
        try:
            self.channel.basic_publish(exchange=exchange_name,
                                       body=json.dumps(message),
                                       routing_key=routing_key)
        except Exception as e:
            logger.error("Exception MSG:", str(e))
