from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import validates
# from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Account(Base):
    __tablename__ = "accounts"


    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text("now()"))

    bio = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)

    validated = Column(Boolean, nullable=False, default=False)
    
    # Adding a check constraint to enforce minimum username length
    __table_args__ = (CheckConstraint("length(username) >= 3", name="min_username_length"),)
    
    @validates("username")
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be 3 characters or longer.")
        return username
