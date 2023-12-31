#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from os import path
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.

        Returns:
            dict: The dictionary __objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        Args:
            obj: The object to be set.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        serialized_objs = {
            k: v.to_dict()
            for k, v in self.__objects.items()
        }
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists).
        Otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised.
        """
        try:
            if path.exists(self.__file_path):
                with open(self.__file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for obj in data.values():
                        cls_name = obj["__class__"]
                        del obj["__class__"]
                        self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return
