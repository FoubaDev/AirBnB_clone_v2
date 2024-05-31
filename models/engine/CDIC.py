#!/usr/bin/python3
""" Db storage Module for HBNB project. """
from os import getenv
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import city, place, review, state, amenity, user


class DBStorage:
    """Db storage class."""
    __engine = None
    __session = None
    CDIC = {
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'Amenity': amenity.Amenity,
        'User': user.User
    }

    def __init__(self):
        """Init an instance of object."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
                                            getenv('HBNB_MYSQL_USER'),
                                            getenv('HBNB_MYSQL_PWD'),
                                            getenv('HBNB_MYSQL_HOST'),
                                            getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

    def reload(self):
        """Reload function."""
        Base.metadata.create_all(self.__engine)
        the_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(the_session)
        self.__session = session()

    def new(self, obj):
        """Define new object."""
        self.__session.add(obj)

    def save(self):
        """save the instance of object."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an instance of object."""
        if obj is not None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """Retrieve all instances of object."""
        obj_dct = {}
        qry = []
        if cls is None:
            for cls_typ in DBStorage.CDIC.values():
                qry.extend(self.__session.query(cls_typ).all())
        else:
            if cls in self.CDIC.keys():
                cls = self.CDIC.get(cls)
            qry = self.__session.query(cls)
        for obj in qry:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dct[obj_key] = obj
        return obj_dct

    def gettables(self):
        """Get the tables."""
        inspector = inspect(self.__engine)
        return inspector.get_table_names()

    def close(self):
        """Close session."""
        self.__session.close()

    def hcf(self, cls):
        """Hcf an instance of object."""
        metadata = MetaData()
        metadata.reflect(bind=self.__engine)
        table = metadata.tables.get(cls.__tablename__)
        self.__session.execute(table.delete())
        self.save()
