import redis
import json
import os
import logging

from dotenv import load_dotenv
from mock_db import get_session

print("Program Started")

load_dotenv()

logging.basicConfig(
    filename="app.log",
    level=logging.INFO
)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

try:

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        socket_connect_timeout=2,
        socket_timeout=2,
        decode_responses=True
    )

    session = redis_client.get("session:101")

    if session:
        response = {
            "source": "redis",
            "status": "success",
            "data": session
        }
    else:
        response = {
            "source": "redis",
            "status": "cache_miss",
            "data": None
        }

except redis.exceptions.TimeoutError:

    logging.error("Redis timeout")

    response = {
        "source": "fallback_mock_db",
        "status": "redis_timeout",
        "data": get_session(101)
    }

except redis.exceptions.ConnectionError:

    logging.error("Redis unavailable")

    response = {
        "source": "fallback_mock_db",
        "status": "redis_unreachable",
        "data": get_session(101)
    }

print(json.dumps(response, indent=4))