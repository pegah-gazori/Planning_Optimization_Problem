"""
File Name: tasks.py
* Django App Name: frontier
* Description:
  This file includes the Celery the task which is used by ReceiveLocations API in the views.py file.
"""

from celery.utils.log import get_task_logger
from planning_optimization_problem import celery_app
from .utils import (create_distance_matrix, format_routing_input)
from planning_optimization_problem.publisher import Publisher
from planning_optimization_problem.settings import (RABBITMQ_INBOUND_QUEUE, RABBITMQ_INBOUND_EXCHANGE,
                                                    RABBITMQ_INBOUND_ROUTING_KEY)

logger = get_task_logger(__name__)


@celery_app.task(name="generate_routing_data", retry_limit=5, default_retry_delay=10)
def task_generate_routing_data(data):
    """
    * Function/Task Name: task_generate_routing_data
    * Description: This function calculates the distance matrix based on the latitude and longitude points of each location
     point and after formatting the input data, it publishes the input message to the inbound queue.
    * Parameter:
        - data: dict
    :return: True
    """
    distance_matrix = create_distance_matrix(locations=data["geographical_coordinations"])
    logger.error(f"The distance matrix is calculated.")
    input_routing_message = format_routing_input(request_id=data["request_id"],
                                                 distance_matrix=distance_matrix,
                                                 num_vehicles=data["num_vehicles"],
                                                 depot=data["depot"])
    message_publisher = Publisher()
    message_publisher.publish(exchange_name=RABBITMQ_INBOUND_EXCHANGE,
                              queue_name=RABBITMQ_INBOUND_QUEUE,
                              routing_key=RABBITMQ_INBOUND_ROUTING_KEY,
                              message=input_routing_message)

    logger.error(f"The routing input message is calculated and published to the {RABBITMQ_INBOUND_QUEUE}.")
    return True
