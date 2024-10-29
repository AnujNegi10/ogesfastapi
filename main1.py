from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
app = FastAPI()

@app.get('/')
def index():
    # return 'hello'
    return {"data":{
        "name": "anuj"
    }}

@app.get('/about') #!'/about' is called here path , get --> is called operation, '@app' is called path operation decorator
def about(): #! path operation function 
    return {"about":{
        "name": "about me"}}

#! fastapi reads request and goes line by line

#! what is swager UI : localhost/docs , it also have /redoc to see routes 

#! pydantic : Pydantic is a Python library used primarily for data validation and data parsing 
#@ Pydantic models allow you to define data structures with strict type checking
#! pydantic ensures username is a string, email is a valid email, and age is an integer. Any incorrect data type or invalid email will raise an error automatically.
#@ Pydantic can parse data into a Python object. For example, it can automatically convert incoming JSON data to Python types, so you don't have to handle conversions manually

@app.get('/id/unpublish')
def blog():
    return {'this is the blog'}

@app.get('/id/{id}')
def getid(id:int):
    return {'Id is ' :id}

@app.get('/id/{id}/comments')
def getid(id):
    return {'Id is ' :{'1','2'}}


#! querry parameter : http://127.0.0.1:8000/blog?limit=30&published=true , are parameters present in the function

#! ? to take values in querry parameter , & to seprate 

@app.get('/blog')
def index(limit , published:bool):
    if published :
        return {'data' : f'{limit} published blogs from db'}
    else:
        return {f'{limit} from the db'}

#! blog Model
class Blog(BaseModel):
    #! creates a schema
    title: str
    body: str 
    published : Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    # return request
    return {'data':f"this is post title {request.title}"}

#! mainly used for debugging process
# if __name__ == '__main__':
#     uvicorn.run(app , host = "127.0.0.1",port=9000)