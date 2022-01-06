"""
* File Name: http_messages.py
* Django App Name: planning_optimization_problem
* Description:
  This file contains a message for each of the HTTP status codes which are used in this project.
"""

__all__ = ['BAD_REQUEST', 'UNPROCESSABLE_ENTITY', 'NOT_FOUND', 'METHOD_NOT_ALLOWED', 'OK']


BAD_REQUEST = "The request body is not of a valid format."
UNPROCESSABLE_ENTITY = "The request body can not be processed."
NOT_FOUND = "The result is not found."
METHOD_NOT_ALLOWED = "This method is not allowed."
OK = "The request has succeeded."
