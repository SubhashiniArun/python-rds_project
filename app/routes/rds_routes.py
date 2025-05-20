from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
import json

from ..utils.rds_instance_connection import create_rds_connection
from ..models import User, Post
from ..marshmallow import UserSchema, PostSchema

api_blueprint = Blueprint('api', __name__)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_rds_connection())

@api_blueprint.route("/test_rds_connection", methods=['GET'])
def test_rds_connection():
    create_rds_connection()
    return jsonify(message="RDS Connection!")


@api_blueprint.route("/users", methods=['GET'])
def get_users():
    # conn = create_rds_connection()
    db = SessionLocal()
    user_data = db.query(User).all()
    # user_data = User.query.all()
    print(f"user data {user_data}")
    return jsonify({
        "message": "User data",
        "data": {user_data}}), 200


@api_blueprint.route("/posts", methods=['GET'])
def get_posts():
    try:
        # conn = create_rds_connection()
        db = SessionLocal()
        # get all 
        # post_data = db.query(Post).all()
        
        # filter_by query
        # post_data = db.query(Post).filter_by(title='Hello World').all()

        # Join Query to get the author/user_id associated with each post
        post_data = db.query(User.name, User.email).join(Post.author).all()

        post_schema = UserSchema(many=True)
        post_data_json = post_schema.dump(post_data)

        
        return jsonify({
        "message": "Post data!",
        "data": post_data_json}), 200
    except Exception as e:
        return jsonify({
            "message": "Error fetching posts",
            "error": {str(e)}
        }), 500
