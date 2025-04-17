from bson import ObjectId

from app.models import Customer, Car, Rental, DBCollections
from pydantic import BaseModel

def create(db_collections: DBCollections, data: BaseModel):
    if isinstance(data, Customer):
        return db_collections.customers.insert_one(data.model_dump())
    elif isinstance(data, Car):
        return db_collections.cars.insert_one(data.model_dump())
    elif isinstance(data, Rental):
        return db_collections.rentals.insert_one(data.model_dump())
    else:
        raise ValueError("Unknown model type")

def get(db_collections: DBCollections, model_type: BaseModel, item_id: str):
    if model_type is Customer:
        value = db_collections.customers.find_one({"_id": ObjectId(item_id)})
    elif model_type is Car:
        value = db_collections.cars.find_one({"_id": ObjectId(item_id)})
    elif model_type is Rental:
        value =  db_collections.rentals.find_one({"_id": ObjectId(item_id)})
    else:
        raise ValueError("Unknown model type")

    if value:
        value["_id"] = str(value["_id"])
    return value


def update(db_collections: DBCollections, model_type: BaseModel, item_id: str, update_data: dict):
    if not isinstance(item_id, ObjectId):
        item_id = ObjectId(item_id)

    if model_type is Customer:
        result = db_collections.customers.update_one({"_id": item_id}, {"$set": update_data})
    elif model_type is Car:
        result = db_collections.cars.update_one({"_id": item_id}, {"$set": update_data})
    elif model_type is Rental:
        result = db_collections.rentals.update_one({"_id": item_id}, {"$set": update_data})
    else:
        raise ValueError("Unknown model type")

    return result.modified_count

