import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sity = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    the_product_of_interest = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    balance = sqlalchemy.Column(sqlalchemy.String, default='0', nullable=True)
    date_reg = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    user_invite = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), default=0)
    is_invite = sqlalchemy.Column(sqlalchemy.String, default='No', nullable=True)
    balance_friend = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    all_balance_in = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    all_balance_out = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)

    user_product_list = orm.relationship("UserProductList", back_populates='user')
    user_history_buy = orm.relationship("UserHistoryBuy", back_populates='user')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    