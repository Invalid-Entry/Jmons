from re import compile
from typing import Callable

_commands = {}


def add_command(regex: str, func: Callable) -> None:
    reg = compile(regex)
    _commands[reg] = func


def print_commands():
    print(_commands)


def find_command(message):
    for key, val in _commands.items():
        if key.match(message):
            return val
