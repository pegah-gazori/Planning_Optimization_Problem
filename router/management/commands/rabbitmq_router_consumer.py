"""
* File Name: rabbitmq_router_consumer.py
* Django App Name: router
* Description:
  This file contains a RabbitMQ consumer that is placed at the server side and is responsible for consuming data messages
  from the inbound queue and then remove them from this queue. It then calls the 'task_prepare_optimal_route_data' task through
  its callback function.
"""

import json
import logging
from django.core.management.base import BaseCommand
from planning_optimization_problem.consumer import Consumer
from planning_optimization_problem.settings import (RABBITMQ_INBOUND_QUEUE, RABBITMQ_INBOUND_EXCHANGE,
                                                    RABBITMQ_INBOUND_ROUTING_KEY)

from router.tasks import task_prepare_optimal_route_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "*** The RabbitMQ Router Listener ***"

    def handle(self, *args, **options):
        logger.warning("RabbitMQ Router Consumer is listening ...")
        message_consumer = Consumer()

        def _callback(channel, method, properties, body):
            logger.warning(f"The routing input message is received from  {RABBITMQ_INBOUND_QUEUE}.")
            routing_input = json.loads(body)
            task_prepare_optimal_route_data.apply_async(kwargs={"data": routing_input}, serializer='json')
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.warning(f"Routing input message is removed from {RABBITMQ_INBOUND_QUEUE}.")

        message_consumer.consume(
            queue_name=RABBITMQ_INBOUND_QUEUE,
            exchange_name=RABBITMQ_INBOUND_EXCHANGE,
            routing_key=RABBITMQ_INBOUND_ROUTING_KEY,
            callback=_callback
        )
