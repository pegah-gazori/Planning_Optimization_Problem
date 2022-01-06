"""
File Name: tasks.py
* Django App Name: router
* Description:
  This file includes the Celery task which is used by the rabbitmq_router_consumer.py file.
"""

from celery.utils.log import get_task_logger
from planning_optimization_problem import celery_app
from planning_optimization_problem.publisher import Publisher
from .utils import generate_optimal_path, format_routing_output
from planning_optimization_problem.settings import (RABBITMQ_OUTBOUND_QUEUE, RABBITMQ_OUTBOUND_EXCHANGE,
                                                    RABBITMQ_OUTBOUND_ROUTING_KEY)

logger = get_task_logger(__name__)


@celery_app.task(name="prepare_optimal_route_data", retry_limit=5, default_retry_delay=10)
def task_prepare_optimal_route_data(data):
    """
    * Function/Task Name: task_prepare_optimal_route_data
    * Description: This function calculates the optimal path based on the input data, and after formatting the output data,
    it publishes the output message to the outbound queue.
    * Parameter:
        - data: dict
    :return: True
    """
    optimal_route = generate_optimal_path(data=data)
    output_routing_message = format_routing_output(request_id=data["request_id"],
                                                   optimal_route=optimal_route)
    message_publisher = Publisher()
    message_publisher.publish(exchange_name=RABBITMQ_OUTBOUND_EXCHANGE,
                              queue_name=RABBITMQ_OUTBOUND_QUEUE,
                              message=output_routing_message,
                              routing_key=RABBITMQ_OUTBOUND_ROUTING_KEY)
    logger.warning(f"The routing output message is calculated and published to the {RABBITMQ_OUTBOUND_QUEUE}.")
    return True
