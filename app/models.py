from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1:many relationship ---> 1 user : many posts

# many:many relationship --> many users: many roles
# 1 user --> [work, cook, mom]
# 1 role --> [user1, user2]
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan", passive_deletes=True)
    roles = db.relationship("Role", secondary='user_roles', back_populates='users')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    author = db.relationship("User", back_populates="posts")


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    users = db.relationship("User", secondary='user_roles', back_populates="roles")


db.Table(
    "user_roles",
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)