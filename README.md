# Planning Optimization Problem

**Creator:** Pegah Gazori | **Created:** 2021-12-25 | **Last Modified:** 2022-01-06

The goal of this project is to provide the optimal route for a given set of locations. In other words, the input of this system is a set of geographical coordinations and the output is the cheapest (shortest) sequence of locations. This project is implemented using the following tools:
* Django REST Framework (DRF)
* RabbitMQ
* Celery
* Redis
* Docker

In this project we have two main Django apps that are `frontier` and `router`. In order to avoid complexity, we assume that the frontier app simulates the end-user side microservice and the router app simulates the server side microservice. (For a large-scale and complex project, we have to create separate microservices for each side)
The complete procedure of this project is described in the following table: (For each step, the name of Django App which is responsible for that functionality is mentioned)

|Step|App|Responsibility|
:---|:---|:---|
|1|Frontier|Receiving the input data (including geographical_coordinations, num_vehicles, and depot) from the end-user and returns a `request_id`.|
|2|Frontier|Calculating the `distance_matrix` for the geographical coordinations using `Euclidean distance` formula.|
|3|Frontier|Formatting the input message (including request_id, distance_matrix, num_vehicles, and depot)|
|4|Frontier|Publishing the input message to the `inbound_queue`.|
|5|Router|Consuming the incoming messages which are published to the `inbound_queue` and removing it from the queue.|
|6|Router|Calculating the `optimal_route` for each input message data using the `or-tools` library.|
|7|Router|Formatting the output message (including request_id, and optimal_route)|
|8|Router|Publishing the output message to the `outbound_queue` and removing it from the queue.|
|9|Frontier|Consuming the incoming messages which are published to the `oubound_queue`.|
|10|Frontier|Writing each output message data on the cache in key-value format (key is request_id and value is optimal_route).|
|11|Frontier|Providing final result to the end-user requests based on the `request_id`.|

***
**NOTE 1:** The final result of each end-user request is provided by the `ReceiveLocations` API which should be called by the application front-end using long-polling method.
***


The application APIs are as follows:

|#|API URL|HTTP Method|Functionality|
|:---|:---|:---|:---|
|1|/frontier/|GET|Checks frontier app availability.|
|2|/frontier/receive_locations/|POST|Receive input data from end-user in JSON format.|
|3|/frontier/get_optimal_route/|GET|Providing output data to the end-user according to the request_id.|


#### Project Deployment:

In order to deploy this project, the  docker and docker-compose must be installed on your system. The project can be run in development mode using Django's built in web server using the following commands:
    
    $ cd Planning_Optimization_Problem
    $ docker-compose build
    $ docker-compose up
 

#### Project Testing:   

In order to test this project before deploying by docker-compose, you can use the following command:
    
    $ python manage.py test --verbosity 2
    
 
If you want to run tests after deploying by docker-compose, use the following sommand:

    $ docker-compose exec app python manage.py test
    
*** 
**NOTE 2:** Test applications are just for evaluating the frontier app view functions. Other tests will be added in the future. 
***
 
*** 
**NOTE 3:** The `wait-for-it` file is a pure bash script that will wait on the availability of a host and TCP port. It can be found in the [wait-for-it](https://github.com/vishnubob/wait-for-it) Github link. It is used in this project to synchronize the spin-up of linked docker containers.
***