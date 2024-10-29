from fastapi import FastAPI
from pydantic import BaseModel

class Blog(BaseModel):
    title:str 
    body: str 


class Showblog(BaseModel):
    title:str
    class Config():
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str 

class ShowUser(BaseModel):
    name:str 
    email: str
    class Config():
        from_attributes = True

class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None