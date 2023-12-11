#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel


def parse_arguments(argument_string):
    curly_braces = re.search(r"\{(.*?)\}", argument_string)
    brackets = re.search(r"\[(.*?)\]", argument_string)
    if curly_braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(argument_string)]
        else:
            lexer = split(argument_string[:brackets.span()[0]])
            return [item.strip(",") for item in lexer] + [brackets.group()]
    else:
        lexer = split(argument_string[:curly_braces.span()[0]])
        return [item.strip(",") for item in lexer] + [curly_braces.group()]


class HBNBCommand(cmd.Cmd):
    """Command interpreter class.
    Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    SUPPORTED_CLASSES = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Exits the program on EOF (Ctrl+D)
        """
        print()  # Print a new line before exiting
        return True

    def emptyline(self):
        """
        Called when an empty line is entered.
        Does nothing to avoid executing the previous command again.
        """
        pass

    def default(self, argument):
        """Default behavior for cmd module when input is invalid"""
        command_mapping = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", argument)
        if match is not None:
            argument_list = [argument[:match.span()[0]], argument[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argument_list[1])
            if match is not None:
                command = [argument_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in command_mapping:
                    call = "{} {}".format(argument_list[0], command[1])
                    return command_mapping[command[0]](call)
        print("*** Unknown syntax: {}".format(argument))

    def do_create(self, argument):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arguments = parse_arguments(argument)
        if not arguments:
            print("** class name missing **")
        elif arguments[0] not in HBNBCommand.SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        else:
            new_instance = eval(arguments[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, argument):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arguments = parse_arguments(argument)
        obj_dict = storage.all()
        if not arguments:
            print("** class name missing **")
        elif arguments[0] not in HBNBCommand.SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        elif len(arguments) == 1:
            print("** instance id missing **")
        elif f"{arguments[0]}.{arguments[1]}" not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[f"{arguments[0]}.{arguments[1]}"])

    def do_destroy(self, argument):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes an instance based on the class name and id.
        """
        arguments = parse_arguments(argument)
        obj_dict = storage.all()
        if not arguments:
            print("** class name missing **")
        elif arguments[0] not in HBNBCommand.SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        elif len(arguments) == 1:
            print("** instance id missing **")
        elif f"{arguments[0]}.{arguments[1]}" not in obj_dict:
            print("** no instance found **")
        else:
            del obj_dict[f"{arguments[0]}.{arguments[1]}"]
            storage.save()
    
    def do_all(self, argument):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        arguments = parse_arguments(argument)
        if arguments and arguments[0] not in HBNBCommand.SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        else:
            obj_list = [str(obj) for obj in storage.all().values() if not arguments or obj.__class__.__name__ == arguments[0]]
            print(obj_list)
    
    def do_count(self, argument):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        arguments = parse_arguments(argument)
        count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == arguments[0])
        print(count)

    def do_update(self, argument):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        arguments = parse_arguments(argument)
        obj_dict = storage.all()
        
        if not arguments:
            print("** class name missing **")
            return False
        if arguments[0] not in HBNBCommand.SUPPORTED_CLASSES:
            print("** class doesn't exist **")
            return False
        if len(arguments) == 1:
            print("** instance id missing **")
            return False
        if f"{arguments[0]}.{arguments[1]}" not in obj_dict:
            print("** no instance found **")
            return False
        if len(arguments) == 2:
            print("** attribute name missing **")
            return False
        if len(arguments) == 3:
            try:
                type(eval(arguments[2])) != dict
            except NameError:
                print("** value missing **")
                return False
            
        obj = obj_dict[f"{arguments[0]}.{arguments[1]}"]
        
        if len(arguments) == 4:
            if arguments[2] in obj.__class__.__dict__ and type(obj.__class__.__dict__[arguments[2]]) in {str, int, float}:
                value_type = type(obj.__class__.__dict__[arguments[2]])
                obj.__dict__[arguments[2]] = value_type(arguments[3])
            else:
                obj.__dict__[arguments[2]] = arguments[3]
        elif type(eval(arguments[2])) == dict:
            for key, value in eval(arguments[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value

        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
