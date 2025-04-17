from fastapi import APIRouter, Request, Response, HTTPException
from app.models import Customer
from app.crud import create, get, update

router = APIRouter()

@router.post("/customers/")
async def create_customer(customer: Customer, request: Request):
    db_collections = request.app.state.db_collections
    customer_id = create(db_collections, customer)
    return {"id": str(customer_id)}

@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str, request: Request):
    db_collections = request.app.state.db_collections
    customer = get(db_collections, Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/customers/{customer_id}")
async def update_customer(customer_id: str, customer: Customer, request: Request):
    db_collections = request.app.state.db_collections

    # Prepare update_data from the customer object
    update_data = customer.dict(exclude_unset=True)

    modified_count = update(db_collections, Customer, customer_id, update_data)
    if modified_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found or nothing changed")

    return {"modified": modified_count}
