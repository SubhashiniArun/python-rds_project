# from flask import Flask

# from app.models import db, Post, Role, User
# from app.config import get_config


# app = Flask(__name__)
# app.config.from_object(get_config("development"))
# db.init_app(app)


# with app.app_context():
#     # db.session.query(User).delete()
#     # db.session.query(Post).delete()
#     # db.session.query(Role).delete()

#     # Create roles
#     # admin_role = Role(name="admin")
#     editor_role = Role(name="editor")

#     # Create users
#     # alice = User(name="Alice", email="alice@example.com", roles=[admin_role, editor_role])
#     # bob = User(name="Bob", email="bob@example.com", roles=[editor_role])
#     john = User(name="John", email="john@example.com", roles=[editor_role])

#         # Create posts
#     # post1 = Post(title="Hello World", content="First post", author=alice)
#     # post2 = Post(title="Second Post", content="More content", author=alice)
#     # post3 = Post(title="Bob's Post", content="Post by Bob", author=bob)

#     db.session.add(john)
#     # db.session.add_all([alice, bob])
#     # db.session.add_all([post1, post2, post3])
#     db.session.commit()
#     print("Seeded users with users, posts, roles.")