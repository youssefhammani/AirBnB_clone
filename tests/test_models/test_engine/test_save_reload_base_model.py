#!/usr/bin/python3
"""Module for testing save and reload methods of BaseModel class."""
from models import storage
from models.base_model import BaseModel
import os
import json


all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new object --")
my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
my_model.save()
print(my_model)

if os.path.exists("file.json"):
    with open("file.json", 'r', encoding='utf-8') as file:
        print(file.read())
