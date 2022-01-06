"""
* File Name: __init__.py
* Django App Name: frontier
* Description:
  This Django app is assumed to be placed at the end-user side. Because of this, it is mainly responsible for:
    1- Receiving data (locations, vehicle(s), depot) from the end-user using POST method.
    2- Pre-processing the location data and calculate the Euclidean distance for each location point (latitude and longitude)
    using celery worker.
    3- Generating the routing data dictionary and then publish the input data message to the inbound queue.
    4- Receiving output messages from the outbound queue and writing them on the cache.
    5- Delivering the optimal route to the end-user.
"""