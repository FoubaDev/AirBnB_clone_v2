#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone."""
import json
from models import city, place, review, state, amenity, user
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format."""
    __file_path = 'file.json'
    __objects = {}
    CDIC = {
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'Amenity': amenity.Amenity,
        'User': user.User
    }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        if cls specified, only returns that class."""
        if cls is not None:
            if cls in self.CDIC.keys():
                cls = self.CDIC.get(cls)
            spec_rich = {}
            for key, value in self.__objects.items():
                if cls == type(value):
                    spec_rich[key] = value
            return spec_rich
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary."""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file."""
        with open(FileStorage.__file_path, 'w') as file:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, file)

    def reload(self):
        """Loads storage dictionary from file."""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """If obj deletes obj from __objects."""
        try:
            key = obj.__class__.__name__ + "." + obj.id
            del self.__objects[key]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Close the session."""
        self.reload()
