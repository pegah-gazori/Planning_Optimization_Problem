"""
* File Name: helper_functions.py
* Django App Name: frontier
* Description:
  This file contains helper functions that are used to create and delete mock data for the test.
"""

import random
from planning_optimization_problem.redis import (write_cache, delete_cache)


def generate_mock_input_data(number_of_locations, number_of_vehicles):
    """
    * Function Name: generate_mock_input_data
    * Description: This function is used to create a random dictionary of input data.
    * Parameters:
        - number_of_locations: int
        - umber_of_vehicles: int
    :return: A dictionary of input data (including geographical_coordinations, num_vehicles, and depot)
    """
    number_of_locations = number_of_locations
    number_of_vehicles = number_of_vehicles
    user_input_data = dict()
    locations_list = list()
    for location_id in range(number_of_locations):
        locations_instance = dict()
        locations_instance["id"] = location_id
        locations_instance["lat"] = random.randint(-100, 100)
        locations_instance["lon"] = random.randint(-100, 100)
        locations_list.append(locations_instance)
    user_input_data["geographical_coordinations"] = locations_list
    user_input_data["num_vehicles"] = number_of_vehicles
    user_input_data["depot"] = random.randint(0, number_of_locations)
    return user_input_data


def write_mock_output_data(request_id, response):
    """
    * Function Name: write_mock_output_data
    * Description: This function is used to write a mock output data (or optimal route) on the redis cache.
    * Parameters:
        - request_id: str
        - response: list
    """
    write_cache(request_id, response)


def delete_mock_output_data(request_id):
    """
    * Function Name: delete_mock_output_data
    * Description: This function is used to delete a mock output data (or optimal route) from the redis cache.
    This will prevent the main cache from being consumed by the test data.
    * Parameter:
        - request_id: str
    """
    delete_cache(request_id)
