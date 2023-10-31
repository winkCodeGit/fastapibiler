__author__ = "Fahad Siddiqui"
__created__ = "23rd-Feb-2023"
__modified__ = "23rd-Feb-2023"

import pandas as pd
import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine

from utility.utilconfig import dbconfig


class Postgres:
    def __init__(self):
        self.params = dbconfig(section="postgresql")

        self.conn = create_engine(
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
                user=self.params["user"],
                password=self.params["password"],
                host=self.params["host"],
                port=self.params["port"],
                database=self.params["database"],
            )
        )

        self.threaded_postgreSQL_pool = pool.ThreadedConnectionPool(
            1,
            68,
            user=self.params["user"],
            password=self.params["password"],
            host=self.params["host"],
            port=self.params["port"],
            database=self.params["database"],
        )

    try:

        def create_connection(self):

            if self.threaded_postgreSQL_pool:
                print(
                    "Connection pool created successfully using ThreadedConnectionPool"
                )
                # Use getconn() method to Get Connection from connection pool
                ps_connection = self.threaded_postgreSQL_pool.getconn()
                return ps_connection

        def get_df(self, query, params):
            print(query)
            if self.threaded_postgreSQL_pool:
                ps_connection = self.create_connection()
                print("successfully recived connection from connection pool ")
                if ps_connection:
                    df = pd.read_sql(query, ps_connection, params=params)
                    ps_connection.close()
                # Use this method to release the connection object and send back ti connection pool
                self.threaded_postgreSQL_pool.putconn(ps_connection)
                print("Put away a PostgreSQL connection")
                return df

        def execute_query(self, query):
            print(query)
            if self.threaded_postgreSQL_pool:
                print("successfully recived connection from connection pool ")
                ps_connection = self.create_connection()
                if ps_connection:
                    ps_cursor = ps_connection.cursor()
                    ps_cursor.execute(query)
                    ps_connection.commit()
                    ps_cursor.close()
                # Use this method to release the connection object and send back ti connection pool
                self.threaded_postgreSQL_pool.putconn(ps_connection)
                print("Put away a PostgreSQL connection")
                return True

        def insert_query(self, columns,data,table):
            """
            Inserts the df records to  table
            param: columns
            param: data
            param: cursor - connection
            """
            if self.threaded_postgreSQL_pool:
                print("successfully recived connection from connection pool ")
                ps_connection = self.create_connection()
                if ps_connection:
                    ps_cursor = ps_connection.cursor()
                    data = ["'" + str(x) + "'" for x in data]
                    q = (
                        """INSERT INTO public.users ({columns}) VALUES ({data});"""
                    ).format(columns=",".join(columns), data=",".join(data))
                    ps_cursor.execute(q)
                    return True

        def execute_select_query(self, query):
            """

            :param conn:
            :param query:
            :return:
            """
            if (
                "update" in query.lower()
                or "delete" in query.lower()
                or "drop" in query.lower()
            ):
                msg = f"Only SELECT query is allowed.\n{query} is not valid."
                raise ValueError(msg)
            try:
                if self.threaded_postgreSQL_pool:
                    print("successfully recived connection from connection pool ")
                    ps_connection = self.create_connection()
                    if ps_connection:
                        ps_cursor = ps_connection.cursor()
                        ps_cursor.execute(query)
                        records = ps_cursor.fetchall()
                        ps_cursor.close()
                    self.threaded_postgreSQL_pool.putconn(ps_connection)
                    print("Put away a PostgreSQL connection")
                    return records

            # except NotFoundError as e:
            #     raise NotFoundError(e)
            except ValueError as e:
                msg = f"Exception while executing query.\nError :- {e}"
                print(msg)
                raise ValueError(e)
            except Exception as e:
                msg = f"Exception while executing query.\nError :- {e}"
                print(msg)
                raise Exception(e)

        def get_all(self, schema_name: str, table_name: str):
            """
            :param conn:
            :param schema_name:
            :param table_name:
            :return:
            """
            try:
                if self.threaded_postgreSQL_pool:
                    print("successfully recived connection from connection pool ")
                    ps_connection = self.create_connection()
                    if ps_connection:
                        ps_cursor = ps_connection.cursor()
                        query = f"SELECT * from {schema_name}.{table_name};"
                        ps_cursor.execute(query)
                        records = ps_cursor.fetchall()
                        ps_cursor.close()
                    self.threaded_postgreSQL_pool.putconn(ps_connection)
                    print("Put away a PostgreSQL connection")
                if records:
                    return records
                else:
                    msg = f"No record found in the table.Check if table have data."
            except Exception as e:
                msg = f"Exception while getting all data from {schema_name}.{table_name} table.\nError :- {e}"
                print(msg)
                raise Exception(msg)

        def get_sql_conn_append(self, df, table_name):
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            return True

        def get_sql_conn_replace(self, df, table_name):
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)


pg_pool = Postgres()