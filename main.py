from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from hubspot import create_contact, sync_contacts
from sqlalchemy import create_engine, Column, DateTime, String, Integer
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from psycopg2.extensions import register_adapter, AsIs
import json

# DB Enviroment
DB_HOST = "db.g97.io"
DB_PORT = 5432
DB_USER = "developer"
DB_PASS = "qS*7Pjs3v0kw"
DB_NAME = "data_analyst"

# HubSpot Token
HUBSPOT_ACCESS_TOKEN = "pat-na1-bfa3f0c0-426b-4f0e-b514-89b20832c96a"

# ClickUp Params
CLICKUP_API_TOKEN = "pk_3182376_Q233NZDZ8AVULEGGCHLKG2HFXWD6MJLC"
CLICKUP_LIST_ID = "900200532843"

# SQLAlchemy Config
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI Def
app = FastAPI()

# Class
class APICall(Base):
    __tablename__ = "api_calls"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    endpoint = Column(String)
    params = Column(String)
    result = Column(String)

class ContactCreateRequest(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: str
    website: str

# Routes
@app.post("/create_contact")
async def create_contact_endpoint(contact: ContactCreateRequest, background_tasks: BackgroundTasks):
    contact_data = {"email": contact.email, "firstname": contact.firstname, "lastname": contact.lastname, "phone": contact.phone, "website": contact.website}
    
    api_call = APICall(
        id=None,
        endpoint="/create_contact",
        params=AsIs("'" + json.dumps(contact_data) + "'")
    )
    db = SessionLocal()
    try:
        create_contact(contact, HUBSPOT_ACCESS_TOKEN)
        api_call.result = "Success"
    except Exception as e:
        api_call.result = f"Error: {str(e)}"
    
    max_id = db.query(func.max(APICall.id)).scalar()
    max_id = max_id if max_id is not None else 0
    new_id = max_id + 1
    api_call.id = new_id
    db.add(api_call)
    db.commit()

    background_tasks.add_task(sync_contacts, HUBSPOT_ACCESS_TOKEN, CLICKUP_API_TOKEN, CLICKUP_LIST_ID)


@app.post("/sync_contacts")
async def sync_contacts_endpoint(background_tasks: BackgroundTasks):
    api_call = APICall(
        endpoint="/sync_contacts",
        params=AsIs("'{}'"),
    )
    db = SessionLocal()
    try:
        sync_contacts(HUBSPOT_ACCESS_TOKEN, CLICKUP_API_TOKEN, CLICKUP_LIST_ID)
        api_call.result = "Success"
    except Exception as e:
        api_call.result = f"Error: {str(e)}"
    
    max_id = db.query(func.max(APICall.id)).scalar()
    max_id = max_id if max_id is not None else 0
    new_id = max_id + 1
    api_call.id = new_id
    db.add(api_call)
    db.commit()