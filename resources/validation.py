__author__ = "Fahad Siddiqui"
__created__ = "23rd-Feb-2023"
__modified__ = "23rd-Feb-2023"

from utility.database import pg_pool
from fastapi import HTTPException, status
import json

def validate(data) -> json:
    query = f"SELECT batch_no, manufacturing_date, expiry_date, quantity FROM batch_validation WHERE batch_no='{data.batch_no}' and manufacturing_date='{data.manufacturing_date}' and expiry_date='{data.expiry_date}' and quantity='{data.quantity}'"
    try:
        df = pg_pool.execute_select_query(query)
        data ={
            "status_code":200,
            "message":"Validated successfully"
        }
        if len(df) == 0:
            raise HTTPException(
                status_code=400,
                detail="Not validated"
            )
    except Exception as e:
        print(e)
        return e
    return data



  

