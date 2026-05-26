import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

engine = None
Base = declarative_base()

def generate_url(user, host, database):
    password = os.getenv("db_password")
    password = "Welcome1"
    print(f"Password: {password}")
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
    return connection_string

def get_engine(user="postgres", host="localhost", database="postgres"):
    global engine
    if engine:
        return engine
    
    url = generate_url(user, host, database)
    engine = create_engine(url)
    return engine