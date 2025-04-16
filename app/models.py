from pydantic import BaseModel
from dataclasses import dataclass
from pymongo.collection import Collection
from pymongo.database import Database

class Customer(BaseModel):
    name: str
    email: str

class Car(BaseModel):
    kilometers_driven: int
    is_rented: bool

class Rental(BaseModel):
    customer_id: str
    car_id: str

@dataclass(frozen=True)
class DBCollections:
    db: Database
    customers: Collection
    cars: Collection
    rentals: Collection
