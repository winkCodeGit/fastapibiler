__author__ = "Fahad Siddiqui"
__created__ = "23rd-Feb-2023"
__modified__ = "23rd-Feb-2023"

from utility.database import pg_pool
from fastapi import HTTPException, status
import json

def login(userdata) -> json:
    query = f"SELECT username, firstname, lastname, email, active FROM users WHERE username='{userdata.username}' and password='{userdata.password}'"
    try:
        df = pg_pool.execute_select_query(query)
        if len(df) == 0:
            raise HTTPException(
                status_code=400,
                detail="Incorrect username or password"

            )
        data = {
            "status_code":200,
            "username":list(df[0])[0],
            "firstname":list(df[0])[1],
            "lastname":list(df[0])[2],
            "email":list(df[0])[3],
        }
    except Exception as e:
        print(e)
        return e

    return data

def is_user_exist(username,email) -> json:
    try:
        is_user = {
            "is_exit":False,
            "message":""
        }
        query= f"select username,email from users WHERE username='{username}' or email='{email}'"
        df = pg_pool.execute_select_query(query)
        if len(df) > 0:
            if list(df[0])[0] == username:
                is_user["message"] = "Username already exist."
                is_user["is_exit"] = True

            if list(df[0])[1] == email:
                is_user["message"] = "Email already exist."
                is_user["is_exit"] = True
            
            if list(df[0])[0] == username and list(df[0])[1] == email:
                is_user["message"] = "Both username and email already exist."
                is_user["is_exit"] = True
   
    except Exception as e:
        print(e)
    return is_user



def signup(userdata) -> json:
    try:
        is_user = is_user_exist(userdata.username,userdata.email)
        data ={
            "userCreated":False,
            "message":""
        }
        if is_user["is_exit"]:
            data["message"] =  is_user["message"]
        else:
            query=f"INSERT INTO users (username,password,firstname,lastname,mobile,email) VALUES ('{userdata.username}','{userdata.password}','{userdata.firstname}','{userdata.lastname}','{userdata.mobile}','{userdata.email}')"
            df = pg_pool.execute_query(query)
            if df:
                data["userCreated"]=True
                data["message"]="user created successfully."

    except Exception as e:
        print(e)
    return data

  

