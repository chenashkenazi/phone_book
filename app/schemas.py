from pydantic import BaseModel, constr
import uuid


class ContactBase(BaseModel):
    first_name: constr(max_length=30)
    last_name: constr(max_length=30)
    phone_number: constr(pattern=r'^\d{9}$')
    address: constr(max_length=40)
    is_favorite: bool = False


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: constr(max_length=30) = None
    last_name: constr(max_length=30) = None
    phone_number: constr(pattern=r'^\d{9}$') = None
    address: constr(max_length=40) = None
    is_favorite: bool = None


class ContactOut(ContactBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
