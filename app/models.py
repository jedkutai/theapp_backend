import re
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
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

    public_account = Column(Boolean, nullable=True, default=True)
    validated = Column(Boolean, nullable=False, default=False)
    
    # Adding a check constraint to enforce minimum username length
    __table_args__ = (
        CheckConstraint("length(username) >= 3", name="min_username_length"),
        CheckConstraint("length(username) <= 16", name="max_username_length"),
        CheckConstraint("username ~ '^[a-zA-Z0-9]*$'", name="alphanumeric_username"),
        )
    
    @validates("username")
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be 3 characters or longer.")
        
        if len(username) > 16:
            raise ValueError("Username cannot be longer than 16 characters.")
        
        if not re.match("^[a-zA-Z0-9]*$", username):
            raise ValueError("Username can only contain letters and numbers.")
        
        return username


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False)
    caption = Column(String, nullable=True)
    image = Column(String, nullable=False)
    game = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text("now()"))

    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Account")

    __table_args__ = (
        CheckConstraint("length(caption) <= 2200", name="max_caption_length"),
        )