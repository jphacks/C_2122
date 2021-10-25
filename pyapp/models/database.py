from app import engine
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import backref, relationship
from flask_login import UserMixin

class UserTable(UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    user_password = Column(String)


class PurposeTable(UserMixin):
    __tablename__ = "purposes"
    id = Column(Integer, nullable=False, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
    user_id = Column(Integer, ForeignKey("UserTable.id"))
    content = Column(String)
    reserved_id = Column(Integer)
    # テーブルの関連を定義
    UserTable = relationship(
        "UserTable", backref=backref("purposes", order_by=id))


class ReserveTable(UserMixin):
    __tablename__ = "reserves"
    id = Column(Integer, nullable=False, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
    purpose_id = (Integer, ForeignKey("PurposeTable.id"))
    # テーブルの関連を定義
    PurposeTable = relationship(
        "PurposeTable", backref=backref("reserves", order_by=id))


class ChatTable(UserMixin):
    __tablename__ = "chats"
    reserve_id = Column(Integer, ForeignKey("ReserveTable.id"))
    date = Column(DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
    content = Column(String)
    user_id_sender = Column(Integer, ForeignKey("UserTable.id"))
    # テーブルの関連を定義
    ReserveTable = relationship(
        "ReserveTable", backref=backref("chats", oder_by=id))
    UserTable = relationship(
        "UserTable", backref=backref("chats", order_by=id))

def create_database():
    Base.metadata.create_all(bind=engine, checkfirst=False)
