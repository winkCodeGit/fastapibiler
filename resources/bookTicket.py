__author__ = "Fahad Siddiqui"
__created__ = "25th-March-2023"
__modified__ = "25th-March-2023"

from utility.database import pg_pool
from fastapi import HTTPException, status
from datetime import datetime
import json
import requests

def sendMail(uniqId):
    url = "https://api.flydreamzz.in/sendMails/" 
    headers = {
            "Content-Type": "application/json", 
        }
    data = {
        "uniqId":uniqId
    }
    response = requests.post(url, json=data, headers=headers)

def bookTicket(data,background_tasks) -> json:
    try:
        no_adult = len(data.passanger_details.adults)
        no_child = len(data.passanger_details.children)
        no_infant = len(data.passanger_details.infants)
        total_ticket = no_adult+no_child
        print(data.passanger_details)
        if no_adult ==0 and no_child ==0:
            return {
                "message":"No child or Adult is Selcted"
            }
        if no_infant > 1:
            return {
                "message":"Only one infant per booking"
            }

        url = "https://api.flydreamzz.in/bookTicketAPI/" 
        headers = {
            "Content-Type": "application/json", 
        }
        data = {
            "params":{
                "username":"agent.yash0",
                "bookingid":data.ticket_id,
                "passagengerDetails":{
                    "adults":data.passanger_details.adults,
                    "children":data.passanger_details.children,
                    "infants":data.passanger_details.infants
                },
                "tickesQuantity":total_ticket,
            }
            
            }
        response = requests.post(url, json=data, headers=headers)
        final_response = response.json()
        if type(final_response) == str:
            final_response1 = final_response
        else:
            final_response1 = {
                "message":final_response["message"],
                "pnr":final_response["pnr"]
            }
            # run background task here
            background_tasks.add_task(sendMail,final_response["uniqId"])
            print(final_response["uniqId"])
        return final_response1
    except Exception as e:
        print(e)