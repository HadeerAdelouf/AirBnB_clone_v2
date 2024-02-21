#!/usr/bin/python3
"""Database storage"""
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv


class DBStorage:
    """Database storage class
    Attributes: __engine, __session
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Method that queries on the currect database session"""
        objects_dic = {}

        if cls is None:
            objs_list = self.__session.query(State).all()
            objs_list.extend(self.__session.query(City).all())
            objs_list.extend(self.__session.query(User).all())
            objs_list.extend(self.__session.query(Place).all())
            objs_list.extend(self.__session.query(Review).all())
            objs_list.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs_list = self.__session.query(cls).all()

        for obj in objs_list:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects_dic[key] = obj

        return objects_dic

    def new(self, obj):
        """adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Method that creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        my_session = sessionmaker(bind=self.__engine,
                                  expire_on_commit=False)
        Session = scoped_session(my_session)
        self.__session = Session()

    def close(self):
        """Method that closes the session"""
        self.__session.close()
