#!/usr/bin/python3
"""
Unittests for the BaseModel class.
"""

import models
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """

    def test_instance_creation(self):
        """
        Test the creation of a BaseModel instance.
        """
        my_model = BaseModel()
        self.assertIsInstance(my_model, BaseModel)

    def test_str_method(self):
        """
        Test the __str__ method of the BaseModel class.
        """
        my_model = BaseModel()
        value = "[BaseModel] ({}) {}".format(my_model.id, my_model.__dict__)
        string_representation = value
        self.assertEqual(str(my_model), string_representation)

    def test_save_method(self):
        """
        Test the save method of the BaseModel class.
        """
        my_model = BaseModel()
        initial_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(initial_updated_at, my_model.updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method of the BaseModel class.
        """
        my_model = BaseModel()
        obj_dict = my_model.to_dict()
        self.assertIsInstance(obj_dict, dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertIn('id', obj_dict)


if __name__ == "__main__":
    unittest.main()
