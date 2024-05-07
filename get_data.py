from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

def create_spark_session():
    return(
        SparkSession
        .builder
        .appName("Flights")
        .master("local[5]")
        .getOrCreate()
    )

spark = create_spark_session()
url=f"https://airlabs.co/api/v9/flights?api_key={os.environ.get("API_KEY")}"
flightrawdata = requests.request('GET', url)
with open('./data/flightdata.json', 'w') as f:
    f.write(str(flightrawdata.json()))

print(flightrawdata.json())


# Stop spark session
spark.stop()
print("spark session stopped")
