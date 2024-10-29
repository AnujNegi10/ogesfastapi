from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,database,models,token
from .. hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends() , db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Input")
    
    if not Hash.verify(user.password,request.password):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")

    
    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token":access_token, "token_type": "bearer"}