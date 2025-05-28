from flask import Blueprint, jsonify, redirect, url_for, session
from flask_login import current_user, login_required, login_user
from authlib.integrations.requests_client import OAuth2Session
from requests.exceptions import HTTPError
import base64

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
import json
import os
from dotenv import load_dotenv

load_dotenv()

from ..utils.rds_instance_connection import create_master_rds_connection, create_slave_rds_connection
from ..utils.encryption import encrypt_token, decrypt_token
from ..models import User, Post, Role, db
from ..oauth import oauth
from ..marshmallow import UserSchema, PostSchema, UserPostCountSchema

api_blueprint = Blueprint('api', __name__)

MasterSession = sessionmaker(autocommit=False, autoflush=False, bind=create_master_rds_connection())
SlaveSession = sessionmaker(autocommit=False, autoflush=False, bind=create_slave_rds_connection())

google = oauth.register(
    name="google",
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"access_type": "offline"},
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "email profile"},
)

def refresh_google_access_token(user):
    refresh_token = user.refresh_token_encrypted
    if not refresh_token:
        raise Exception("No refresh token available")

    # Use your app's OAuth2 client config
    client = oauth.create_client('google')  # or oauth.google if already registered
    token_url = client.access_token_url

    session = OAuth2Session(client.client_id, client.client_secret)
    new_token = session.refresh_token(
        url=token_url,
        refresh_token=refresh_token,
    )

    # Save new access token (and refresh_token if it changes)
    user.access_token = new_token['access_token']
    if 'refresh_token' in new_token:
        user.refresh_token = new_token['refresh_token']
    
    db.session.commit()

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify(
        {"message": "Flask API Working"}
    )

@api_blueprint.route("/login")
def login():
    redirect_uri = url_for("api.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@api_blueprint.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()

    # stmt = select(User).filter_by(User.email == user_info['email']).first()
    with MasterSession() as db_session:
        # result = session.execute(stmt).mappings.all()
        user = db_session.query(User).filter_by(email = user_info['email']).first()
        if not user:
            user = User(
                name=user_info['name'],
                email=user_info['email'],
                provider="google",
                provider_id=user_info['id'],
                access_token_encrypted=encrypt_token(token['access_token']),
                refresh_token_encrypted=encrypt_token(token['refresh_token'])
            )
            db_session.add(user)
            db_session.commit()

            login_user(user)
        session['user'] = {"name": user.name, "email": user.email}
    return redirect('profile')

    
@api_blueprint.route('/profile')
@login_required
def get_profile():
    try:
        # Create session with current user's token
        token = {
            'access_token': decrypt_token(current_user.access_token_encrypted),
            'token_type': 'Bearer',
        }
        google = OAuth2Session(token=token)
        response = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
        response.raise_for_status()

    except HTTPError as e:
        if e.response.status_code == 401:
            # Attempt to refresh the token
            refresh_google_access_token(current_user)

            # Retry with new token
            token = {
                'access_token': decrypt_token(current_user.access_token_encrypted),
                'token_type': 'Bearer',
            }
            google = OAuth2Session(token=token)
            response = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
            response.raise_for_status()
        else:
            raise
    return jsonify(f"This is the Profile Page for the user {current_user.name}")


@api_blueprint.route("/test_rds_connection", methods=['GET'])
def test_rds_connection():
    create_master_rds_connection()
    create_slave_rds_connection()
    return jsonify(message="RDS Connection Established!")


@api_blueprint.route("/users", methods=['GET'])
def get_users():
    """ Queries using select / session.execute() """
    stmt = select(User.name)
    stmt2 = select(User.name, User.email, Post.title).join(Post, User.id == Post.user_id)

    stmt3 = (
        select(
        Post.user_id, func.count(Post.id).label('post_count')
        ).group_by(Post.user_id).subquery()
    )

    stmt4 = (
        select(User.name, stmt3.c.post_count).select_from(User.__table__.join(stmt3, User.id == stmt3.c.user_id))
    )
    
    with SlaveSession() as session:
        user = session.query(User).filter_by(email = "subhashini258@gmail.com").first()
        result = session.execute(stmt).mappings().all()
        user_schema = UserSchema(many = True)

        result2 = session.execute(stmt2).mappings().all()

        user_post_count_schema = UserPostCountSchema(many=True)
        result3 = session.execute(stmt4).mappings().all()
        user_post_count_json = user_post_count_schema.dump(result3)

    """ Queries using db.query() """
    # db = SlaveSession()
    # # get all user data
    # user_data = db.query(User).all()

    # # Join Query to get the author/user_id associated with each post
    # user_data = db.query(User.name, User.email, Post.title).join(Post, Post.user_id == User.id).all()
    # print(f"user data before dump {user_data}")
    # user_data_json = [user._asdict() for user in user_data]
    # # user_schema = UserSchema(many=True)
    # # user_data_json = user_schema.dump(user_data)

    # user_role_query = db.query(User.id, User.name, Role.name).join(user_roles, User.roles==Role.id).all()
    # print(f"user_role_query data before dump {user_role_query}")

    # print(f"user data {user_data_json}")
    return jsonify({
        "message": "User data",
        "data": user_post_count_json}), 200


@api_blueprint.route("/posts", methods=['GET'])
def get_posts():
    try:
        # db = SlaveSession()

        # # get all post data
        # # post_data = db.query(Post).all()
        
        # # filter_by query
        # post_data = db.query(Post).filter_by(title='Hello World').all()

        # post_schema = PostSchema(many=True)
        # post_data_json = post_schema.dump(post_data)

        return jsonify({
            "message": "Post data!",
            "data": "hello"}), 200
    except Exception as e:
        return jsonify({
            "message": "Error fetching posts",
            "error": {str(e)}
        }), 500
