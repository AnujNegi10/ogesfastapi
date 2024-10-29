from fastapi import APIRouter,Depends
from .. import schemas,database,models,oauth2
from typing import List
from sqlalchemy.orm import Session
router  = APIRouter()

@router.get('/allblog',response_model=List[schemas.Showblog])
def all(db:Session = Depends(database.get_db),get_current_user: schemas.User= Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs 