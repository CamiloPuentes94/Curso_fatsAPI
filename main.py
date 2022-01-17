# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie
from  fastapi import status

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    
    first_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50,
        example= "Andrea"
    )
    last_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50,
        example= "Cervera Lozano"
    )
    age: int = Field(
        ...,
        gt=0,
        le=100,
        example= 31
    )
    hair_color: Optional[HairColor] = Field(default=None, example= "black")
    is_married: Optional[bool] = Field(default=None, example=True)

class Person(PersonBase):
    
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    
    username: str = Field(
        ...,
        max_length=20,
        example="migue2022"
        )
    message: str = Field(
        default="Login successfully"
        )

@app.get(
    path= "/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):   #esta clase me dice que es de tipo body, cuando en los parametros tienen ... quiere decir que es obligatorio
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description= "This is the person name. It's between 1 and 50 characters",
        example="Samantha"
        ),
    age: str = Query(
        ...,
        title= "Person age",
        description= "this is the person age. It's requered",
        example="1"
        )
):
    return {name: age}

# Validaciones: path parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt= 0,
        title= "Person id",
        description= "this is the person id. It's obligatory",
        example=2134
        ) 
):
    return {person_id: "It exist!"}

# validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the person ID",
        gt=0,
        example=2134
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and headers parameters

@app.post(
    path= "/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1 
    ),
    last_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1 
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length= 20
    ),
    user_agent: Optional[str] = Header(default= None),
    ads: Optional[str] = Cookie(default= None)
):
    return user_agent