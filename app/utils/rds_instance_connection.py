from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

rds_username = os.getenv('RDS_USERNAME')
rds_password = os.getenv('RDS_PASSWORD')
master_rds_database = os.getenv('MASTER_RDS_DATABASE')
master_rds_endpoint = os.getenv('MASTER_RDS_ENDPOINT')
slave_rds_database = os.getenv('SLAVE_RDS_DATABASE')
slave_rds_endpoint = os.getenv('SLAVE_RDS_ENDPOINT')

def create_master_rds_connection():
    master_engine = create_engine(f"mysql+pymysql://{rds_username}:{rds_password}@{master_rds_endpoint}:3306/{master_rds_database}")
    # conn = engine.connect()
    
    return master_engine


def create_slave_rds_connection():
    slave_engine = create_engine(f"mysql+pymysql://{rds_username}:{rds_password}@{slave_rds_endpoint}:3306/{slave_rds_database}")
    # conn = engine.connect()
    
    return slave_engine


