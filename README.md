# autoverleih
Car rental management application, supporting customer and car management, and rental operations

## Stack used

- **Backend:** FastAPI
- **Database:** MongoDB
- **Frontend:** HTML

## ▶How to Run
> Requires Python 3.9+ and MongoDB (local or Atlas).

```bash
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run project
python main.py

# .env file
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_CLUSTER=
MONGO_APP_NAME=

MONGO_DB_NAME=
MONGO_CUSTOMERS_COLLECTION=
MONGO_CARS_COLLECTION=
MONGO_RENTALS_COLLECTION=


