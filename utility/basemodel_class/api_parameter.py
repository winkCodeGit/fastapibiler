__author__ = "Fahad Siddiqui"
__created__ = "23rd-Feb-2023"
__modified__ = "23rd-Feb-2023"

import json
from typing import *
from pydantic import BaseModel, validator
from datetime import datetime



class Person(BaseModel):
    gender: str
    firstname: str
    lastname: str


class Adult(Person):
    isWheel: bool


class Child(Person):
    dob: str

    # @validator('dob')
    # def validate_dob(cls, dob):
    #     try:
    #         datetime.strptime(dob, '%d-%m-%Y')
    #     except ValueError:
    #         raise ValueError('Incorrect date format, should be DD-MM-YYYY')
    #     return dob


class Infant(Person):
    dob: str

    # @validator('dob')
    # def validate_dob(cls, dob):
    #     try:
    #         datetime.strptime(dob, '%d-%m-%Y')
    #     except ValueError:
    #         raise ValueError('Incorrect date format, should be DD-MM-YYYY')
    #     return dob

class PassengerDetails(BaseModel):
    adults: List[dict] = []
    children: List[dict] = []
    infants: List[dict] = []

class ticketfilter(BaseModel):
    airportFrom:Optional[str] = None
    airportTo:Optional[str] = None
    travelDate:Optional[str] = None

class traveldata(BaseModel):
    """
    class
    pydantic basemodal class to get travel details
    adults: [
        {gender: "MR./MS./MRS.", firstname: "John", lastname: "Doe", isWheel: true/false}],
        children: [{gender: 'Master./Miss.', firstname: 'John', lastname: 'Doe', dob: '01-04-2021'}],
        infants: [{gender: 'Infant.', firstname: 'John', lastname: 'Doe', dob: '02-04-2023'}], 
    """
    ticket_id:str
    passanger_details:PassengerDetails
