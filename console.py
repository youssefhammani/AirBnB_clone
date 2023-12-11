#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class.
    """

    prompt = "(hbnb) "

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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
