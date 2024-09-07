from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from fastapi import HTTPException, status, Response
import uuid
from app.logging_config import log_function


def sort_contacts(contacts, favorites=False):
    sorted_contacts = sorted(contacts, key=lambda x: x.first_name.lower())
    if favorites:
        sorted_contacts = sorted(sorted_contacts, key=lambda x: not x.is_favorite)
    return sorted_contacts


@log_function
def get_contacts(db: Session, page: int = 1, limit: int = 10, favorites: bool = False):
    total_count = db.query(models.Contact).count()
    query = db.query(models.Contact)
    offset = (page - 1) * limit
    contacts = query.offset(offset).limit(limit).all()
    sorted_contacts = sort_contacts(contacts=contacts, favorites=favorites)
    next_skip = offset + limit if offset + limit < total_count else None
    previous_skip = offset - limit if offset - limit >= 0 else None

    base_url = "/contacts"
    next_page = f"{base_url}/?limit={limit}&page={page+1}" if next_skip is not None else None
    previous_page = f"{base_url}/?limit={limit}&page={page-1}" if previous_skip is not None else None

    response = {
        "contacts": sorted_contacts,
        "total_count": total_count,
        "limit": limit,
        "page": page,
        "next": next_page,
        "previous": previous_page
    }

    return response


@log_function
def create_contact(db: Session, contact: schemas.ContactCreate):
    try:
        if db.query(models.Contact).filter(models.Contact.phone_number == contact.phone_number).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Contact with the same phone number exists.")

        new_contact = models.Contact(**contact.dict())
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Contact with the same phone number exists.")


@log_function
def search_contacts(db: Session, search_text: str):
    words = search_text.split()
    query = db.query(models.Contact)

    for word in words:
        search_word = f"%{word}%"
        query = query.filter(
            models.Contact.first_name.ilike(search_word) |
            models.Contact.last_name.ilike(search_word) |
            models.Contact.phone_number.ilike(search_word)
        )

    return query.all()


@log_function
def delete_contact(db: Session, contact_id: uuid.UUID):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@log_function
def update_contact(db: Session, contact_id: uuid.UUID, contact_data: schemas.ContactUpdate):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if contact_data.phone_number is not None:
        same_phone_number = db.query(models.Contact).filter(
            models.Contact.phone_number == contact_data.phone_number).first()
        if same_phone_number:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Contact with the same phone number exists.")
    if not contact_data.model_dump(exclude_unset=True).items():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid fields.")

    for key, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact
