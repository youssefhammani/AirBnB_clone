#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_arguments(arg_str):
    curly_braces = re.search(r"\{(.*?)\}", arg_str)
    brackets = re.search(r"\[(.*?)\]", arg_str)
    if curly_braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(arg_str)]
        else:
            lexer = split(arg_str[:brackets.span()[0]])
            return [item.strip(",") for item in lexer] + [brackets.group()]
    else:
        lexer = split(arg_str[:curly_braces.span()[0]])
        return [item.strip(",") for item in lexer] + [curly_braces.group()]


class HBNBCommand(cmd.Cmd):
    """Command interpreter class.
    Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __SUPPORTED_CLASSES = {
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
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        Exits the program on EOF (Ctrl+D).
        """
        print()  # Print a new line before exiting
        return True

    def emptyline(self):
        """
        Called when an empty line is entered.
        Does nothing to avoid executing the previous command again.
        """
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        command_mapping = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in command_mapping.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return command_mapping[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args = parse_arguments(arg)
        if not args:
            print("** class name missing **")
        elif args[0] not in self.__SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        else:
            new_instance = eval(args[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = parse_arguments(arg)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.__SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes an instance based on the class name and id.
        """
        args = parse_arguments(arg)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.__SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        args = parse_arguments(arg)
        if len(args) > 0 and \
                args[0] not in self.__SUPPORTED_CLASSES:
            print("** class doesn't exist **")
        else:
            obj_list = [
                str(obj)
                for obj in storage.all().values()
                if not args or obj.__class__.__name__ == args[0]
            ]
            print(obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = parse_arguments(arg)
        count = sum(
            1
            for obj in storage.all().values()
            if obj.__class__.__name__ == args[0]
        )
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        arguments = parse_arguments(arg)
        obj_dict = storage.all()

        if not arguments:
            print("** class name missing **")
            return False
        if arguments[0] not in self.__SUPPORTED_CLASSES:
            print("** class doesn't exist **")
            return False
        if len(arguments) == 1:
            print("** instance id missing **")
            return False
        if f"{arguments[0]}.{arguments[1]}" not in obj_dict.keys():
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
            if (
                arguments[2] in obj.__class__.__dict__ and
                type(obj.__class__.__dict__[arguments[2]]) in {str, int, float}
            ):
                value_type = type(obj.__class__.__dict__[arguments[2]])
                obj.__dict__[arguments[2]] = value_type(arguments[3])
            else:
                obj.__dict__[arguments[2]] = arguments[3]
        elif type(eval(arguments[2])) == dict:
            for key, value in eval(arguments[2]).items():
                if (
                    key in obj.__class__.__dict__.keys() and
                    type(obj.__class__.__dict__[key]) in {str, int, float}
                ):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value

        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
