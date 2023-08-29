from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/account",
    tags=["Account"]
)


@router.get("/")
def root():
    return {"message": "User Portal"}





@router.post("/createaccount", status_code=status.HTTP_201_CREATED, response_model=schemas.AccountCreateOut)
def create_account(account: schemas.AccountCreateIn, db: Session = Depends(get_db)):
    
    try:
        account.password = utils.hash_password(account.password)
        new_account = models.Account(**account.model_dump())

        db.add(new_account)
        db.commit()
        db.refresh(new_account)
    
    except Exception as e:
        if "accounts_email_key" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        if "accounts_username_key" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    
    return new_account




@router.post("/viewaccount", response_model=schemas.AccountViewOut) # , response_model=schemas.AccountViewOut
def view_account(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    account = db.query(models.Account).filter(models.Account.id == current_user.id).first()
    
    return account




@router.delete("/deleteaccount")
def delete_account():
    return {"message": "Delete Acount"}


@router.post("/recoveraccount")
def recover_account():
    return {"message": "Recover Account"}

