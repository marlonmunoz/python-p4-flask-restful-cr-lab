from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    name = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Float)

    id = db.Column(db.Integer, primary_key=True)
