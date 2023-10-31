__author__ = "Fahad Siddiqui"
__created__ = "25th-March-2023"
__modified__ = "25th-March-2023"

import uvicorn
from fastapi import FastAPI,UploadFile,Header,Depends,HTTPException,BackgroundTasks
from pydantic import BaseModel
import cv2
import numpy as np
from fastapi.responses import JSONResponse
from pyzbar.pyzbar import decode
from resources.authentication import *
from resources.ticketdetails import *
from resources.bookTicket import *
from utility.basemodel_class.api_parameter import *
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import time
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import base64
from fastapi.openapi.utils import get_openapi

tags_metadata = [
    {
        "name": "Ticket Details",
        "description": """
            Get ticket details
            URL: https://test.flydreamzz.in/ticket-detail
            Payload:(optional)
                travel_date : '2023-04-28' (Please use given format for travel date)
                airport_from : 'CCU' (Standard airport code in capital)
                airport_to: 'HYD'    (Standard airport code in capital)
            Method: GET
            Header:
                secret-key: "test",   #given secret key
            Response:
                [
                    {
                    "airline": "Air Asia",
                    "flight_no": "I5 992",
                    "travel_date": "2023-04-28",
                    "departure_time": "22:25:00",
                    "arrival_time": "12:50:00",
                    "airport_from": "BLR",
                    "airport_to": "CCU",
                    "available_seats": 4,
                    "deal": "5700",
                    "ticket_id": "dash1632"
                    }
                ]
        """,
    },
    {
        "name": "Ticket Booking",
        "description": """
                Book ticket
                URL :https://test.flydreamzz.in/ticket-booking
                Method: POST
                Header:
                    secret-key: "test" (given secret key)
                Payload: {
                    bookingid:"dash2344",   (id received in get ticket)
                    passanger_details:{
                    adults: [
                        {
                            gender: "MR./MS./MRS.",
                            firstname: "John", 
                            lastname: "Doe", 
                            isWheel: true/false
                        }
                    ], 
                    children: [
                        {
                            gender: 'Master./Miss.',
                            firstname: 'John',
                            lastname: 'Doe',
                            dob: '01-04-2021'
                        }
                    ], 
                    infants: [
                        {
                            gender: 'Infant.',
                            firstname: 'John',
                            lastname: 'Doe', 
                            dob: '02-04-2023'
                            }
                    ]
                }
                    
                }
            NOTE: Pass children and infant as empty list/Array if not avialable
                example:
                        {
                    bookingid:"dash2344",   (id received in get ticket)
                    passanger_details:{
                    adults: [
                        {
                            gender: "MR./MS./MRS.",
                            firstname: "John", 
                            lastname: "Doe", 
                            isWheel: true/false
                        }
                    ], 
                    children: [], 
                    infants: []
                }
            }
            Response:
                Suceess or Failed 

        """
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
     {
        "name": "Availabe Date",
        "description": """
            Get ticket details
            URL: https://test.flydreamzz.in/sector?sector=CCU-DEL
            Payload:
                sector : CCU-DEL (Standard airport code in capital separated by '-')
            Method: GET
            Header:
                secret-key: "test",   #given secret key
            Response:
                ["2023-05-09","2023-05-10"]
        """,
    },
]

description = """
<img src="https://flydreamzz.in/static/media/loginLogo.dbb22f85.jpg" alt="flydreamzz image" width="400" height="300">
"""



app = FastAPI(title="Flydreamzz API",
    description=description,
    version="0.0.1",
    terms_of_service="https://flydreamzz.in",
    contact={
        "name": "Frlydreamzz",
        "url": "https://flydreamzz.in",
        "email": "support@flydreamzz.in",
    },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    openapi_tags=tags_metadata
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "test"

def getSecretkey(secretKey) -> json:
    try:
        query =f"SELECT appuser_secretkey.secretkey,appuser_secretkey.test_secretkey, auth_user.username FROM appuser_secretkey JOIN auth_user ON appuser_secretkey.user_id = auth_user.id WHERE secretkey = '{secretKey}'"
        df = pg_pool.execute_select_query(query)
        is_valid = False
        if len(df) > 0:
            username = df[0][2]
            # decode secret key 
            decode_msg = base64.b64decode(secretKey).decode()
            user = decode_msg.split("username:")[1]
            if user.strip() == username.strip():
                is_valid = True
        return is_valid
    except Exception as e:
        print(e)

@app.middleware("http")
async def authenticate(request, call_next):
    isvalid_user = getSecretkey(request.headers.get("secret-key"))
    if request.url.path.startswith("/redoc") or request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        response = await call_next(request)
    else:
        if isvalid_user == False:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    response = await call_next(request)
    return response

async def get_token_header(secret_key: str = Header(...)):
    return secret_key


# @app.get("/ticket-detail")
# async def get_ticket_details(secret_key: dict = Depends(get_token_header)):
#     url = "https://api.flydreamzz.in/getDashboard/" 
#     headers = {
#         "Content-Type": "application/json", 
#     }
#     data = {
#         "filters":{},
#         "username":"fahadsiddiqui707@gmail.com"
#         }
#     response = requests.post(url, json=data, headers=headers)
#     return response.json()

@app.get("/ticket-detail",tags=["Ticket Details"])
async def ticket_details(secret_key: dict = Depends(get_token_header),travel_date:str='none',airport_from:str='none',airport_to:str='none'):
    data = getTicketDetail(travel_date,airport_from,airport_to)
    return data

@app.post("/ticket-booking",tags=["Ticket Booking"])
async def book_ticket(data:traveldata,background_tasks: BackgroundTasks,secret_key: dict = Depends(get_token_header)):
    res = bookTicket(data,background_tasks)
    return res

@app.get("/sector",tags=["Availabe Date"])
async def sector_search(sector:str,secret_key: dict = Depends(get_token_header)):
    data = get_all_date_for_sector(sector)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3033)
        
