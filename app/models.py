from sqlalchemy import Column, String, Boolean, UUID, Index
from sqlalchemy.dialects.postgresql import UUID as pgUUID
import uuid
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone_number = Column(String(9), nullable=False, unique=True)
    address = Column(String(40))
    is_favorite = Column(Boolean, default=False)

    __table_args__ = (
        Index('idx_first_name', 'first_name'),
        Index('idx_last_name', 'last_name'),
    )
