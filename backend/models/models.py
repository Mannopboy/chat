from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, DateTime, or_, and_, desc, func, ARRAY, JSON, \
    extract
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
from pprint import pprint
from datetime import datetime

db = SQLAlchemy()


def db_setup(app):
    """
    to connect flask app and flask sqlalchemy package and migrate sqlalchemy models
    :param app:
    :return:
    """
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class User(db.Model):
    """
    A class to create user db table

    relationship:
        UsersMessages table to get all messages
    """
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    messages = relationship("UsersMessages", backref="user", order_by=desc("UsersMessages.id"))
    status = Column(DateTime)
    img = Column(String)

    def add(self):
        """
        to add new item and commit it
        :return: new item
        """
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """
        to update item
        :return: updated item
        """
        db.session.commit(self)

    def delete(self):
        """
        to delete item
        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class UserContacts(db.Model):
    """
    A class to create contact table
    foreign key:
        first_person: user who saves contact,
        second_person: to get another user data
    backref:
        first: get first user's date from User model
        second: get second user's date from User model
    """
    __tablename__ = "users_contacts"
    id = Column(Integer, primary_key=True)
    first_person = Column(Integer, ForeignKey('user.id'))
    second_person = Column(Integer, ForeignKey('user.id'))
    first = relationship("User", foreign_keys=[first_person])
    second = relationship("User", foreign_keys=[second_person])
    name = Column(String)
    img = Column(String)

    def add(self):
        """
        to add new item and commit it
        :return: new item
        """
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """
        to update item
        :return: updated item
        """
        db.session.commit(self)

    def delete(self):
        """
        to delete item
        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class UsersChat(db.Model):
    """
    A class to create chat table
    foreign keys:
        first_person: user who first writes message
        second_person: user who first receives message
    backref:
        first: get first user's date from User model
        second: get second user's date from User model
    relationship:
        UsersMessages:  model to get all messages by chat id
    """
    __tablename__ = "users_chat"
    id = Column(Integer, primary_key=True)
    first_person = Column(Integer, ForeignKey('user.id'))
    second_person = Column(Integer, ForeignKey('user.id'))
    first = relationship("User", foreign_keys=[first_person])
    second = relationship("User", foreign_keys=[second_person])
    messages = relationship('UsersMessages', backref="user_chat", order_by="UsersMessages.id")

    def convert_json(self, user=None):
        """
            api function
            :return: model UsersChat datas in object form
        """
        if user.id != self.second_person:
            username = self.second.username
            img = self.second.img
        else:
            username = self.first.username
            img = self.first.img
        num_not_seen = UsersMessages.query.filter(UsersMessages.chat_id == self.id,
                                                  UsersMessages.messages_status == None,
                                                  UsersMessages.user_id != user.id).count()
        date = ''
        last_msg = 'Cleaned Up'

        if self.messages:
            if self.messages[len(self.messages) - 1].text:
                # to get last message by chat id
                last_msg = self.messages[len(self.messages) - 1].text

            # to get last message's created time by comparing current day
            if self.messages[len(self.messages) - 1].date.strftime("%Y-%m-%d") > datetime.now().strftime("%Y-%m-%d"):

                # to get last message's created time by chat id
                date = self.messages[len(self.messages) - 1].date.strftime("%Y-%m-%d")
            else:
                date = self.messages[len(self.messages) - 1].date.strftime("%H:%M")
        return {
            "id": self.id,
            "last_msg": last_msg,
            "date": date,
            "count": num_not_seen,
            "username": username,
            "img": img
        }

    def add(self):
        """
        to add new item and commit it
        :return: new item
        """
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """
        to update item
        :return: updated item
        """
        db.session.commit(self)

    def delete(self):
        """
        to delete item
        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class UsersMessages(db.Model):
    """
    A class to create message table
    foreign keys:
        chat_id: to get id column from chat model
        user_id: to get id from user model
    relationship:
        messages_status: to get SeenMessages datas
    """
    __tablename__ = "users_messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('users_chat.id'))
    text = Column(String)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    messages_status = relationship('SeenMessages', backref="user_msg", order_by="SeenMessages.id")

    def add(self):
        """
        to add new item and commit it
        :return: new item
        """
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """
        to update item
        :return: updated item
        """
        db.session.commit(self)

    def delete(self):
        """
        to delete item
        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class SeenMessages(db.Model):
    """
    A class to create seen_messages table
    this model to separate messages by (received, not received)
    foreign keys:
        user_id: to get id colum from user model
        msg_id: to get id colum from users_messages model
    """
    __tablename__ = "seen_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    msg_id = Column(Integer, ForeignKey('users_messages.id'))

    def add(self):
        """
        to add new item and commit it
        :return: new item
        """
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """
        to update item
        :return: updated item
        """
        db.session.commit(self)

    def delete(self):
        """
        to delete item
        :return: None
        """
        db.session.delete(self)
        db.session.commit()
