from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "mysql+mysqlconnector://root:""@localhost:3306/crudpython"
#engine = create_engine(DATABASE_URL)

DATABASE_URL = 'sqlite:///./crudpython.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo = True)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()