"""
* File Name: __init__.py
* Django App Name: router
* Description:
  This Django app is assumed to be placed at the server side. Because of this, it is mainly responsible for:
    1- Listening to the inbound queue for incoming messages. (includes routing data like distance matrix, vehicle(s), depot)
    2- Calculating the optimal route based on the input data.
    3- Generating the optimal route dictionary and then publish the output data message to the outbound queue.
"""