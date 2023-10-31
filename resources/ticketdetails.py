__author__ = "Fahad Siddiqui"
__created__ = "25th-March-2023"
__modified__ = "25th-March-2023"

from utility.database import pg_pool
from fastapi import HTTPException, status
from datetime import datetime
import json

def get_all_date_for_sector(sector) -> json:
    airportFrom = sector.split('-')[0]
    airportTo = sector.split('-')[1]
    where_query = """
        bookingtype = 'online' 
        AND availableseats > 0 
        AND approved = TRUE 
        AND iscancel = FALSE 
        AND traveldate >= NOW() 
        AND airportfrom.name ='{0}' 
        AND airportto.name ='{1}'
        """.format(airportFrom,airportTo)
    query = """SELECT
        appuser_dashboard.traveldate
    FROM appuser_dashboard
    JOIN appuser_airline 
            ON appuser_dashboard.airlines_id = appuser_airline.id 
        JOIN appuser_airport AS airportfrom 
            ON appuser_dashboard.airportfrom_id = airportfrom.id 
        JOIN appuser_airport AS airportto 
            ON appuser_dashboard.airportto_id = airportto.id
    WHERE 
        {0}""".format(where_query)
    try:
        print(query)
        df = pg_pool.execute_select_query(query)
        datas = []
        for x in df:
            datas.append(x[0])
        data ={
            "status_code":200,
            "data":datas
        }
        if len(df) == 0:
            data = {
                "status_code":200,
                "data":[]
            }
    except Exception as e:
        print(e)
        return e
    return datas

def getTicketDetail(traveldate,airport_from,airport_to) -> json:
    where_query = """
        bookingtype = 'online' 
        AND availableseats > 0 
        AND approved = TRUE 
        AND iscancel = FALSE
        """
    if traveldate == 'none' or traveldate == ' ' or traveldate == "" or traveldate == " " or traveldate== 'string':
        where_query = where_query + " AND traveldate >= NOW()"
    else:
        where_query = where_query + " AND traveldate ='{0}'".format(traveldate)

    if airport_from != 'none' and airport_from != ' ' and airport_from != "" and airport_from != " " and airport_from != 'string':
        where_query = where_query + " AND airportfrom.name ='{0}'".format(airport_from)
    
    if airport_to != 'none' and airport_to != ' ' and airport_to != "" and airport_to != " " and airport_to != 'string':
        where_query = where_query + " AND airportto.name ='{0}'".format(airport_to)

    query = """SELECT
        appuser_airline.name, 
        appuser_dashboard.flightno,
        appuser_dashboard.traveldate,
        appuser_dashboard.departure,
        appuser_dashboard.arrival,
        airportfrom.name AS airportfrom_name,
        airportto.name AS airportto_name,
        appuser_dashboard.availableseats,
        appuser_dashboard.deal,
        appuser_dashboard.bookingid
    FROM 
        appuser_dashboard 
        JOIN appuser_airline 
            ON appuser_dashboard.airlines_id = appuser_airline.id 
        JOIN appuser_airport AS airportfrom 
            ON appuser_dashboard.airportfrom_id = airportfrom.id 
        JOIN appuser_airport AS airportto 
            ON appuser_dashboard.airportto_id = airportto.id  
    WHERE 
        {0}""".format(where_query)
    print("===query",query)
    try:
        df = pg_pool.execute_select_query(query)
        datas = []
        for x in df:
            airlineCode = x[1].split(" ")[0]
            datas.append(
                {
                    "airline":x[0],
                    "flight_no":x[1],
                    "airline_code":airlineCode,
                    "travel_date":x[2],
                    "departure_time":x[3],
                    "arrival_time":x[4],
                    "airport_from":x[5],
                    "airport_to":x[6],
                    "available_seats":x[7],
                    "deal":x[8],
                    "ticket_id":x[9]
                }
                )
        data ={
            "status_code":200,
            "data":datas
        }
        if len(df) == 0:
            data = {
                "status_code":200,
                "data":[]
            }
    except Exception as e:
        print(e)
        return e
    return datas



  

