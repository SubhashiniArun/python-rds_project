from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

rds_username = os.getenv('RDS_USERNAME')
rds_password = os.getenv('RDS_PASSWORD')
rds_database = os.getenv('RDS_DATABASE')
rds_endpoint = os.getenv('RDS_ENDPOINT')

def create_rds_connection():
    engine = create_engine(f"mysql+pymysql://{rds_username}:{rds_password}@{rds_endpoint}:3306/{rds_database}")
    # conn = engine.connect()
    
    return engine



