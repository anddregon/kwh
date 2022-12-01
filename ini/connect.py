from pymongo import MongoClient
from dotenv import dotenv_values


def connect():
    """
    Connect to Firebase.
    """
    # Load environment variables:
    config = dotenv_values('../.env')

    # Connect to MongoDB:
    client = MongoClient(config['ATLAS_URI'])

    # Get database:
    db = client['kwh']

    # Get collection:
    collection = db['data']

    return collection
