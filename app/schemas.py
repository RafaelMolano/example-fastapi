from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

#clase para manejar los atributos que se quieren mostrar al hacer Post, la idea es no mostrar todo el esquema
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    #Mostrar datos relacionados del esquema Usuarios
    owner: UserOut

    #Este es necesario para que al hacer la petición, pydentic sea capaz de transformar la data en un diccionario
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
 
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #Solo permite 0 o 1
    