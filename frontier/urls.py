"""
File Name: urls.py
* Django App Name: frontier
* Description:
  This file includes the URL patterns of the APIViews that are located in the frontier app.
"""

from django.urls import path
from .views import (Ping, ReceiveLocations, GetOptimalRoute)


urlpatterns = [
    path("", Ping.as_view(), name="ping"),
    path("receive_locations/", ReceiveLocations.as_view(), name="receive-locations"),
    path("get_optimal_route/", GetOptimalRoute.as_view(), name="get-optimal-route")
]



