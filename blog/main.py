from typing import List
from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas,models
from .hashing import Hash
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import blog,authentication

# from passlib.context import CryptContext
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.post('/blog',status_code=201)
def create(request:schemas.Blog , db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title , body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}' , status_code=status.HTTP_204_NO_CONTENT)
def destroy(id , db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()

    return 'done'

#! update : Bulk Update

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id , request:schemas.Blog , db: Session = Depends(get_db)):
    blog  = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first(): #!.first(): Executes the query and returns the first matching row from the database, or None if no row matches.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    blog.update(request.dict())
    db.commit()
    
    return 'updated'
    

# @app.get('/allblog',response_model=List[schemas.Showblog])
# def all(db:Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs 

@app.get('/blog/{id}',status_code=200,response_model=schemas.Showblog)
def show(id ,response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not available")


    return blog



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user',response_model= schemas.ShowUser )
def create_user(request: schemas.User , db:Session = Depends(get_db)):

    # hashedPassword = pwd_context.hash(request.password)

    new_user = models.User(name = request.name , email=request.email , password = Hash.bcrypt(request.password) )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser)
def get_user(id:int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user not found with id {id}")
    
    return user

