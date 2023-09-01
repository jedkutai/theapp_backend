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

@router.post("/checkaccount", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.AccountCreateOut)
def create_account(account: schemas.AccountCreateIn, db: Session = Depends(get_db)):
    
    try:
        new_account = models.Account(**account.model_dump())
        
        search_username = db.query(models.Account).filter(models.Account.username == new_account.username).first()
        search_email = db.query(models.Account).filter(models.Account.email == new_account.email).first()
        
        if not search_username and not search_email:
            return new_account
        
        else:
            raise ValueError("Username or email already exists")
    
    except Exception:
        if search_username and not search_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        
        elif not search_username and search_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username and email already exist")
    
    


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
        
        if str(e) == "Username must be 3 characters or longer.":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{str(e)}")
        
        if str(e) == "Username cannot be longer than 16 characters.":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{str(e)}")
        
        if str(e) == "Username can only contain letters and numbers.":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{str(e)}")

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

