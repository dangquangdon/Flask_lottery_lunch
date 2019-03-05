# import uuid
# from datetime import datetime

# from flask import current_app
# from flask_login import UserMixin

# from main import db, login_manager

# class Subscriber(db.Model, UserMixin):

#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(80),
#                           nullable=False,
#                           default=lambda: str(uuid.uuid4()))
#     first_name = db.Column(db.String(80),
#                          nullable=False)
#     last_name = db.Column(db.String(80),
#                          nullable=False)
#     email = db.Column(db.String(80),
#                       nullable=False,
#                       unique=True)
#     password = db.Column(db.String(80),
#                          nullable=False)

#     join_date = db.Column(db.DateTime,
#                           nullable=False,
#                           default=datetime.utcnow)

#     is_admin = db.Column(db.Boolean,
#                          nullable=False,
#                          default=False)

#     pairwith = db.relationship('PairWith', backref='pair', lazy=True)

#     def __repr__(self):
#         return "Subscriber({}, {})".format(self.first_name, self.last_name)

# class PairWith(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     paired_with = db.Column(db.String(80), nullable=False)
#     paired_date = db.Column(db.DateTime,
#                             nullable=False,
#                             default=datetime.utcnow)

#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('subscriber.id'),
#                         nullable=False)


# @login_manager.user_loader
# def load_user(user_id):
#   return Subscriber.query.get(int(user_id))
