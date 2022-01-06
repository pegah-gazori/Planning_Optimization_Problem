"""
File Name: view.py
* Django App Name: frontier
* Description:
  This file includes the APIs which are used by the application end-user to send request and receive intended response.
    1- ReceiveLocations (POST)
    2- GetOptimalRoute (GET)
"""

from rest_framework import status
from .utils import generate_random_uuid
from rest_framework.views import APIView
from .tasks import task_generate_routing_data
from rest_framework.response import Response
from planning_optimization_problem.redis import read_cache
from planning_optimization_problem.http_messages import (BAD_REQUEST, UNPROCESSABLE_ENTITY, NOT_FOUND)


class Ping(APIView):
    def get(self, request):
        """
        * Method Name and Type: get / GET
        * Description: This method is used to check the availability of the frontier app.
        :return: A JSON-formatted response containing the 'pong' string and HTTP status code.
        """
        return Response({"response": "pong"}, status=status.HTTP_200_OK)


class ReceiveLocations(APIView):
    def post(self, request):
        """
        * Method Name and Type: post / POST
        * Description: This method is used to receive the request data from the end-user and start the processing procedure.
        * Parameter:
            - request: JSON object
        :return: A JSON-formatted response message and its related HTTP status code.
        NOTE: If the request is valid, a string 'request_id' will be returned to the end-user to keep tracking of the
        request status and result.
        """
        data = request.data
        if isinstance(data, dict) and len(data) == 0:
            return Response({"response": UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif not isinstance(data, dict):
            return Response({"response": BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request_id = generate_random_uuid()
            data["request_id"] = request_id
            task_generate_routing_data.apply_async(kwargs={"data": data}, serializer='json')
            return Response({"response": request_id}, status=status.HTTP_201_CREATED)


class GetOptimalRoute(APIView):
    def get(self, request):
        """
       * Method Name and Type: get / GET
        * Description: This method is used to reade the result of each end-user request (using reques_id) from the Redis
        cache and if it  is available, return it to the end-user.
        * Parameter:
            - request: str (request_id)
        :return: A JSON-formatted response message and its related status code.
        NOTE: If there is not any error in other parts of the request processing flow, it means that the result of the
        end-user request is not ready yet.
        end-user request is not ready yet.
        """
        request_id = str(request.GET.get("request_id", ""))
        if len(request_id) == 0:
            return Response({"response": BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(request_id, str) and "-" not in request_id:
            return Response({"response": UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            routing_result = read_cache(request.GET.get("request_id"))
            if routing_result:
                return Response({"response": routing_result}, status=status.HTTP_200_OK)
            else:
                return Response({"response": NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
