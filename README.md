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

    SQLALCHEMY_DATABASE_URI is set in the config -> config loaded to the app -> db extensions are initialized

-> use Flask Migrate to automate schema changes to be pushed to AWS RDS 

