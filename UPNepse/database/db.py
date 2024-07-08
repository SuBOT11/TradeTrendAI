from pymongo import MongoClient 
import os 
from dotenv import load_dotenv



def connect_to_mongodb():
    try:
        load_dotenv()

        connection_string = os.getenv('MONGODB_CONN_STRING')
        # Establish connection to MongoDB
        client = MongoClient(connection_string)
        print("Connected to MongoDB successfully")
        return client
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        return None