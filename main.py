# Python
from typing import Optional
from fastapi.param_functions import Query

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):

    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):   #esta clase me dice que es de tipo body, cuando en los parametros tienen ... quiere decir que es obligatorio
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description= "This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title= "Person age",
        description= "this is the person age. It's requered"
        )
):
    return {name: age}

# Validaciones: path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt= 0,
        title= "Person id",
        description= "this is the person id. It's obligatory"
        ) 
):
    return {person_id: "It exist!"}

# validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the person ID",
        gt=0
    ),
    person: Person = Body(...)
):
    return person