from re import compile
from typing import Callable

from tabulate import tabulate

_commands = {}
_reaction_register = {}


def add_command(regex: str, func: Callable) -> None:
    reg = compile(regex)
    _commands[reg] = func


def print_commands() -> None:
    rows = []
    for key, val in _commands.items():
        rows.append([key.pattern, str(val)])

    print(tabulate(rows))


def find_command(message) -> Callable:
    for key, val in _commands.items():
        if key.search(message):
            return val


def add_reaction_register(name, func: Callable) -> None:
    _reaction_register[name] = func


def find_reaction(name):
    return _reaction_register[name]
