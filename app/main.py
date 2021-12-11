from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine
import app.dbconection
from . import models, schemas, utils
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware


#Esta línea se deshabilita al utilizar alembic. Esta línea permite a MySQLAlchemy crear las tablas nuevas (PERO NO los cambios de las mismas)
#models.Base.metadata.create_all(bind=engine)


#newConection = app.dbconection.DBHelper()

app = FastAPI()

#origins = ['https://www.google.com']
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"message": "Hello world"}


