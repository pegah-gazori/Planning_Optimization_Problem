"""
File Name: redis.py
* Django App Name: planning_optimization_problem
* Description:
  This file contains the initializations of the Redis and also contains wrapper functions for its main operations
  (read, write, delete).
"""

import redis
import json
import logging
from planning_optimization_problem.settings import REDIS_HOST


logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)


def read_cache(key):
    """
    * Function Name: read_cache
    * Description: This function is used to read key-value data from Redis cache.
    * Parameters:
        - key: str
    :return: bytes
    """
    try:
        return redis_client.get(key)
    except Exception as e:
        logger.error("Exception MSG:", str(e))
        return False


def write_cache(key, value):
    """
    * Function Name: write_cache
    * Description: This function is used to write a key-value data on the Redis cache.
    NOTE: The key is reguest_id and the value is result of optimal route calculation.
    * Parameters:
        - key: str
        - value: list
    :return: boolean (True/False)
    """
    try:
        redis_client.set(key, json.dumps(value))
        return True
    except Exception as e:
        logger.error("Exception MSG:", str(e))
        return False


def delete_cache(key):
    """
    * Function Name: delete_cache
    * Description: This function is used to delete unused data from the Redis cache.
    * Parameters:
        - key: str
    :return: boolean (True/False)
    """
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error("Exception MSG:", str(e))
        return False
