from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from ..schemas import account_schema
from .. import utils, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

