from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from .models import User, Post, Role

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    
    id = auto_field()
    name = auto_field()
    email = auto_field()
    posts = auto_field()
    roles = auto_field()

class PostSchema(SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True
    
    id = auto_field()
    title = auto_field()
    content = auto_field()
    user_id = auto_field()


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True
    
    id = auto_field()
    name = auto_field()
    users = auto_field()


class UserPostCountSchema(Schema):
    name = fields.String()
    post_count = fields.Integer()