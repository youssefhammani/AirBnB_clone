#!/usr/bin/python3
"""
Module containing the FileStorage class.
"""

import json
from os import path
from models.base_model import BaseModel


class FileStorage:
    """
    Serializes instances to a JSON file
    and deserializes JSON file to instances.
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
                    for key, value in data.items():
                        cls_name, obj_id = key.split('.')
                        obj_instance = eval(cls_name)(**value)
                        self.__objects[key] = obj_instance
        except FileNotFoundError:
            pass
