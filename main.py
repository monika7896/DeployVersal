from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLite database URL
DATABASE_URL = "sqlite:///./test.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Model for Employee
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations using the database

# Create an employee
@app.post("/employees/")
async def create_employee(employee: Employee, db: Session = Depends(get_db)):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

# Get all employees
@app.get("/employees/")
async def read_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# Get a specific employee by name
@app.get("/employees/{employee_name}")
async def read_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == employee_name).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# Update an employee's position
@app.put("/employees/{employee_name}")
async def update_employee_position(employee_name: str, new_position: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == employee_name).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.position = new_position
    db.commit()
    return {"message": f"Position updated for {employee_name}"}

# Delete an employee
@app.delete("/employees/{employee_name}")
async def delete_employee(employee_name: str, db: Session = Depends(get_db)):
    db.query(Employee).filter(Employee.name == employee_name).delete()
    db.commit()
    return {"message": f"Employee {employee_name} deleted"}
