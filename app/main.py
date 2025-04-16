import sys
from urllib.parse import quote_plus
import certifi
from pymongo import errors
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from models import Car, Customer, Rental, DBCollections

def connection_to_database():

    # Credentials for MongoDB
    username = os.getenv('MONGO_USERNAME')
    password = os.getenv('MONGO_PASSWORD')
    cluster = os.getenv('MONGO_CLUSTER')
    app_name = os.getenv('MONGO_APP_NAME')
    username = quote_plus(username)
    password = quote_plus(password)

    uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName={app_name}"

    try:
        # Create a new client and connect to the server
        mongo_client = MongoClient(uri, tlsCAFile=certifi.where())
        mongo_client.admin.command('ping')
        return mongo_client
    except errors.ConfigurationError:
        print("An Invalid URI host error was received!")
        return None

def get_collections(mongo_client):

    db_name = os.getenv("MONGO_DB_NAME")
    customers_collection_name = os.getenv("MONGO_CUSTOMERS_COLLECTION")
    cars_collection_name = os.getenv("MONGO_CARS_COLLECTION")
    rentals_collection_name = os.getenv("MONGO_RENTALS_COLLECTION")

    database = mongo_client[db_name]

    customers_collection = database[customers_collection_name]
    cars_collection = database[cars_collection_name]
    rentals_collection = database[rentals_collection_name]

    created_db_collections = DBCollections(database, customers_collection, cars_collection, rentals_collection)

    return created_db_collections


def test(db_collections):
    # Sample data for customers
    customer1 = Customer(name="John Doe", email="john.doe@example.com")

    # Adding one customer
    try:
        result = db_collections.customers.insert_one(customer1.model_dump())
        print(result.inserted_id)
    except errors.OperationFailure:
        print("An authentication error was received!")

    print("\n")

    # Getting all costumers
    result = db_collections.customers.find()

    if result:
        for costumer in result:
            costumer_id = costumer['_id']
            costumer_name = costumer['name']
            costumer_email = costumer['email']
            print(f"{costumer_id}: {costumer_name} {costumer_email}")
    else:
        print("No documents found.")

    print("\n")

    # Finding a single document
    my_costumer = db_collections.customers.find_one({"name": "John Doe"})

    if my_costumer is not None:
        print(my_costumer)
    else:
        print("I didn't find any costumer like that!")

    print("\n")

if __name__ == "__main__":
    load_dotenv()
    client = connection_to_database()

    if client:
        db_collections_instance = get_collections(client)
        test(db_collections_instance)
    else:
        sys.exit(1)


