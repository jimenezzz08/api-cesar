from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    notes = relationship("Note", back_populates="creator")


class Note(Base):
    __tablename__ = "notes"

    id_tur = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    img_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id_user"))

    creator = relationship("User", back_populates="notes")
