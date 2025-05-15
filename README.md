# Python RDS Project

ORM Models -> SQLAlchemy
AWS RDS Connection -> mysql+pymysql URI
Flask DB setup -> Flask - SQLAlchemy
DB Migrations -> Alembic/Flask Migrate

-> Establish RDS connection using rds instance's 
    user_name
    password
    host/emdpoint
    dbname that we need to establish connection  

-> use Flask Migrate to automate schema changes to be pushed to AWS RDS 

