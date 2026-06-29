import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

engine = None
Base = declarative_base()

def generate_url(user, host, database):
    password = os.getenv("DB_PASSWORD")
    print(f"Password: {password}")
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
    return connection_string

def get_engine(user=os.getenv("DB_USER"), host=os.getenv("DB_HOST"), database=os.getenv("DB_DB")):
    global engine
    if engine:
        return engine
    
    url = generate_url(user, host, database)
    engine = create_engine(url)
    return engine

def table_to_json(table):
    return {c.name: getattr(table, c.name) for c in table.__table__.columns}

def query_result_as_list(result):
    output = []
    for row in result:
        output.append(table_to_json(row))
    return output