"""
* File Name: rabbitmq_frontier_consumer.py
* Django App Name: frontier
* Description:
  This file contains a RabbitMQ consumer that is placed at the end-user side and is responsible for consuming data messages
  from the outbound queue and then remove them from this queue. It then write each message on the Redis cache through its
  callback function  in other to make it accessible for the end-users.
"""

import json
import logging
from django.core.management.base import BaseCommand
from planning_optimization_problem.redis import write_cache
from planning_optimization_problem.consumer import Consumer
from planning_optimization_problem.settings import (RABBITMQ_OUTBOUND_QUEUE, RABBITMQ_OUTBOUND_EXCHANGE,
                                                    RABBITMQ_OUTBOUND_ROUTING_KEY)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "*** The RabbitMQ Frontier Listener ***"

    def handle(self, *args, **options):
        logger.warning("RabbitMQ Frontier Consumer is listening ...")
        message_consumer = Consumer()

        def _callback(channel, method, properties, body):
            logger.warning(f"The routing output message is received from {RABBITMQ_OUTBOUND_QUEUE}.")
            output_routing_message = json.loads(body)
            write_result = write_cache(output_routing_message["request_id"],
                                       output_routing_message["optimal_route"])
            if write_result:
                channel.basic_ack(delivery_tag=method.delivery_tag)
                logger.warning(f"The routing output message is removed from {RABBITMQ_OUTBOUND_QUEUE} and is wrote on the cache.")
            else:
                logger.error("An error was occurred during writing data on the cache.")

        message_consumer.consume(
            queue_name=RABBITMQ_OUTBOUND_QUEUE,
            exchange_name=RABBITMQ_OUTBOUND_EXCHANGE,
            routing_key=RABBITMQ_OUTBOUND_ROUTING_KEY,
            callback=_callback
        )
