"""
File Name: utils.py
* Django App Name: frontier
* Description:
  This file includes the utility functions that are used by the Celery tasks in the tasks.py file.
"""

import uuid
import numpy as np


def generate_random_uuid():
    """
    * Function Name: generate_random_uuid
    * Description: This function is used to provide a random UUID for each of the end-user request. Each request can be
    tracked using it's unique UUID.
    :return: A string UUID
    """
    return str(uuid.uuid4())


def calculate_euclidean_distance(source, destination):
    """
    * Function Name: calculate_euclidean_distance
    * Description: This function is used to calculate the Euclidean distance for each pair of the location points.
    * Parameters:
        - source (location point 1): int or float
        - destination (location point 2): int or float
    :return: A float/int number
    """
    source_location = np.array((source["lat"], source["lon"]))
    destination_location = np.array((destination["lat"], destination["lon"]))
    return np.linalg.norm(source_location - destination_location)


def create_distance_matrix(locations):
    """
    * Function Name: create_distance_matrix
    * Description: This function is used to create the distance matrix for all input location points.
    * Parameters:
        - locations: list (a list of dictionaries)
    :return: A list (a list of lists)
    """
    dimension = len(locations)
    final_matrix = list()
    for i in range(0, dimension):
        row = list()
        for j in range(0, dimension):
            distance = calculate_euclidean_distance(locations[i], locations[j])
            row.append(distance)
        final_matrix.append(row)
    return final_matrix


def format_routing_input(request_id, distance_matrix, num_vehicles, depot):
    """
    * Function Name: format_routing_input
    * Description: This function is used to format the input message before publishing it to the inbound queue.
    * Parameters:
        - request_id: str
        - distance_matrix: list
        - num_vehicles: int
        - depot: int (the location id of depot)
    :return: The input message data dictionary
    """
    data_dictionary = {
        "request_id": request_id,
        "distance_matrix": distance_matrix,
        "num_vehicles": num_vehicles,
        "depot": depot
    }
    return data_dictionary
