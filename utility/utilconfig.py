__author__ = "Fahad Siddiqui"
__created__ = "23rd-Feb-2023"
__modified__ = "23rd-Feb-2023"


from dotenv import load_dotenv
import os


def dbconfig(section='postgresql'):
    if section == 'postgresql':
        load_dotenv()
        # create a database connection
        db = {}
        db['host'] = os.getenv('API_PG_HOST')
        db['port'] = os.getenv('API_PG_PORT')
        db['database'] = os.getenv('API_PG_DB')
        db['user'] = os.getenv('POSTGRES_USER')
        db['password'] = os.getenv('POSTGRES_PASSWORD')
        for item, value in db.items():
            if value is not None:
                continue
            else:
                raise Exception(
                    'Section [{0}] not found in env variable'.format(item)
                )
        return db


if __name__ == '__main__':
    dbconfig()