"""
File Name: utils.py
* Django App Name: frontier
* Description:
  This file includes the utility functions that are used by the Celery tasks in the tasks.py file.
"""

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


def get_routes(solution, routing, manager):
    """
    * Function Name: get_routes
    * Description: This function gets vehicle routes and store them in a two dimensional array whose i,j entry is the
    jth location visited by vehicle i along its route. It receives vehicle routes from a solution and store them in an array
    * Parameters:
        - solution: solution object
        - routing: routing object
        - manager: manager object
    :return: A nested list (list of lists; each list is the optimal route for one vehicle)
    NOTE: In this project, we are using one vehicle for calculations and due to this, we have only one list and we can
    get it through the nested list through the 'routes[0]'. If we have multi vehicles in the project, we must change the
    return value to the 'routes'.
    """
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes[0]  # index 0 is for one vehicle configuration mode. :)


def generate_optimal_path(data):
    """
    * Function Name: generate_optimal_path
    * Description: This function is the entry point for generating optimal route. It creates the routing index manager
     and then creates routing model. Then, it converts each routing variable to distance matrix index. After that, the
     cost of each arc will be defined. At last, the first solution heuristic will be set and the problem will be solved.
     NOTE: The 'distance_callback' function is used convert routing variable index to distance matrix NodeIndex. It returns
     the distance between the two nodes.
    * Parameters:
        - data: dict
    :return: The routes object (which must be processed to generate the optimal route array)
    """
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'],
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    routes = get_routes(solution, routing, manager)
    return routes


def format_routing_output(request_id, optimal_route):
    """
    * Function Name: format_routing_output
    * Description: This function is used to format the output message before publishing it to the outbound queue.
    * Parameters:
        - request_id: str
        - optimal_route: list
    :return: The output message data dictionary
    """
    data_dictionary = {
        "request_id": request_id,
        "optimal_route": optimal_route
    }
    return data_dictionary
