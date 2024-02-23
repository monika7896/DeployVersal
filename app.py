from fastapi import FastAPI
from pydantic import BaseModel
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy import create_engine

app=FastAPI()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine=create_engine(SQLALCHEMY_DATABASE_URL)


# class Employee(BaseModel):
#     _tablename ="employee"
    
#     emp_id=Column(Integer,primary_key=True)
#     emp_name =Column(Strring)
#     emp_dept=Column(String)
#     emp_position=Column(string)
    

# Base.metada.create_all(bind=engine)

@app.get("/employee/{emp_id}")
def getEmp(emp_id):
    return {'name':'monika'}
    # engine.query(employee).filter(emp_id)
    # if 
