from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = "mysql://root:root@localhost/pythonapi?charset=utf8"
SQLALCHEMY_DATABASE_URL = f"mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}?charset=utf8"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {
        "port": settings.database_port
    })

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()