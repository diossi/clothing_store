import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Item(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_down = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type_wear = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    is_see = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)
    count_buy = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
