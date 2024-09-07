from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import engine, get_db
from slowapi import Limiter
from slowapi.util import get_remote_address
import uuid

import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.get("/contacts/")
@limiter.limit("100/minute")
def get_contacts(request: Request, page: int = 1, limit: int = 10, favorites: bool = False, db: Session = Depends(get_db)):
    return utils.get_contacts(db, page=page, limit=limit, favorites=favorites)


@app.post("/contacts/", response_model=schemas.ContactOut)
@limiter.limit("100/minute")
def create_contact(request: Request, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return utils.create_contact(db, contact)


@app.get("/contacts/search/", response_model=list[schemas.ContactOut])
@limiter.limit("100/minute")
def search_contacts(request: Request, search_text: str, db: Session = Depends(get_db)):
    return utils.search_contacts(db, search_text)


@app.delete("/contacts/{contact_id}")
@limiter.limit("100/minute")
def delete_contact(request: Request, contact_id: uuid.UUID, db: Session = Depends(get_db)):
    return utils.delete_contact(db, contact_id)


@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
@limiter.limit("100/minute")
def update_contact(request: Request, contact_id: uuid.UUID, contact_data: schemas.ContactUpdate, db: Session = Depends(get_db)):
    return utils.update_contact(db, contact_id, contact_data)
