# Python RDS Project


* ORM Models -> SQLAlchemy
* AWS RDS Connection -> mysql+pymysql URI
* Flask DB setup -> Flask - SQLAlchemy
* DB Migrations -> Alembic/Flask Migrate

* Establish RDS connection using rds instance's 
    user_name
    password
    host/endpoint
    dbname that we need to establish connection

* SQLALCHEMY_DATABASE_URI is set in the config => config loaded to the app => db extensions are initialized

* use Flask Migrate to automate schema changes to be pushed to AWS RDS 

* Use Marshmallow to serialize the SQLAlchmeny ORM models

* DB queries (SQLAlchemy - select, select_from (subquery), func.coalecse, func.count)

#### OAuth Implementation
* Initialize the app with `oauth=OAuth()` -> `oauth.init_app(app)`
* On `/login`, user will be redirected to google authorization page
* On successful authorization, securely store the access token, refresh token in the DB 
    * encrypt the token['access_token] & token['refresh_token] using the #Fernet(secret_key)#
    * user will be redirected `/profile` page (decorated with @login_required) upon unsuccessful authorization user redirected to `/login` page (google signin)
    * set `login_user(user)` where user is the user queried from DB
    * set `session['user']` to store user name and email
* On 401 error accessing /profile, call `google.refresh_token(url="https://oauth2.googleapis.com/token", refresh_token=<<decrypted_stored_refresh_token>>)` to get new access token and refresh token
    * persist the new access token and refresh token in the DB


## Master Slave Archirecture
* Create a read replica for the primary DB in AWS RDS
* Master DB for writes
* Slave DB for reads
* Writes to Master DB gets asynchronously replicated in the Slave DB



