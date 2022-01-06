"""
* File Name: test_views.py
* Django App Name: frontier
* Description:
  This file contains all the functional tests for evaluating the view functions of the frontier app. Each test case, is
  focused on three step which are as follows:
  - GIVEN: The initial conditions for the test.
  - WHEN: What is occurring that needs to be tested?
  - THEN: What is the expected response?
  NOTE: The Input value of each reverse() method is the URL pattern name.
"""

from django.urls import reverse
from rest_framework import status
from django.test import SimpleTestCase
from ..utils import generate_random_uuid
from rest_framework.test import APITestCase, APIClient
from .helper_functions import (generate_mock_input_data, write_mock_output_data, delete_mock_output_data)

client = APIClient()


class PingViewTest(SimpleTestCase):
    """
    Related APIView Name: Ping
    URL: /frontier/ping/
    """
    def test_frontier_app_availability(self):
        response = self.client.get(reverse("ping"))
        self.assertEqual(response.status_code, 200)


class ReceiveLocationsViewTest(APITestCase):
    """
    Related APIView Name: ReceiveLocations
    URL: /frontier/receive_locations/
    """
    def test_receive_locations_view_with_invalid_http_method(self):
        response = client.get(reverse("receive-locations"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_receive_locations_view_with_invalid_request(self):
        response = client.post(reverse("receive-locations"), data={123}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(reverse("receive-locations"), data={'test'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_receive_locations_view_with_unprocessable_request(self):
        response = client.post(reverse("receive-locations"), data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_receive_locations_view_with_valid_request(self):
        payload = generate_mock_input_data(number_of_locations=10, number_of_vehicles=1)
        response = client.post(reverse("receive-locations"), data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetOptimalRouteViewTest(APITestCase):
    """
    Related APIView Name: GetOptimalRoute
    URL: /frontier/get_optimal_route/
    """
    def test_get_optimal_route_with_with_invalid_http_method(self):
        response = client.post(reverse("get-optimal-route"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_optimal_route_with_invalid_request(self):
        response = client.get(reverse("get-optimal-route"))
        self.assertEqual(response.status_code, 400)

        url = reverse("get-optimal-route") + "?request_id="
        response = client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_optimal_route_with_unprocessable_request_parameter(self):
        url = reverse("get-optimal-route") + "?request_id=13c002b4115c4d65a40aa82472a1a3d8"
        response = client.get(url)
        self.assertEqual(response.status_code, 422)

    def test_get_optimal_route_with_unavailable_request_parameter(self):
        url = reverse("get-optimal-route") + "?request_id=" + generate_random_uuid()
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_optimal_route_with_valid_request_parameter(self):
        mock_request_id = generate_random_uuid()
        mock_response = [7, 3, 4, 5, 6, 2, 0, 8, 9, 1, 7]
        write_mock_output_data(mock_request_id, mock_response)
        url = reverse("get-optimal-route") + "?request_id=" + mock_request_id
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        delete_mock_output_data(mock_request_id)
