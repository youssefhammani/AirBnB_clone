#!/usr/bin/python3
"""
Module containing the BaseModel class.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Defines the BaseModel class for other classes to inherit from.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(value, date_format))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            # storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation of the BaseModel instance.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute 'updated_at'
        with the current datetime.
        """
        self.updated_at = datetime.now()
        # storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.

        Returns:
            dict: Dictionary representation of the BaseModel instance.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    @classmethod
    def from_dict(cls, obj_dict):
        """
        Recreates an instance from a dictionary representation.

        Args:
            obj_dict (dict): Dictionary representation of the instance.

        Returns:
            BaseModel: Recreated instance.
        """
        if '__class__' in obj_dict:
            obj_dict.pop('__class__')
        return cls(**obj_dict)
