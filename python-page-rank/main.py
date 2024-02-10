import os
from dotenv import load_dotenv
import redis

def main():
  # Load environment variables from .env file
  load_dotenv()

  # Get Redis connection details from environment variables
  redis_host = os.getenv("REDIS_HOST")
  redis_port = os.getenv("REDIS_PORT")
  redis_password = os.getenv("REDIS_PASSWORD")

  # Connect to Redis
  r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

  # Test the connection
  try:
    r.ping()
    print("Connected to Redis successfully!")
  except redis.ConnectionError:
    print("Failed to connect to Redis.")
    return

if __name__ == "__main__":
  main()