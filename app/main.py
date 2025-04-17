import sys
import uvicorn
from dotenv import load_dotenv
from app.mongo_database import connection_to_database, get_collections, test
from routes.customers import router as customers_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


if __name__ == "__main__":
    load_dotenv()
    client = connection_to_database()

    if client:
        app.state.db_collections = get_collections(client)
        app.include_router(customers_router)
        # test(db_collections_instance)
    else:
        sys.exit(1)

    uvicorn.run(app, host="0.0.0.0", port=8000)