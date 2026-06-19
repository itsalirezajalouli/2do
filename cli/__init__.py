import readline
import re
from io import StringIO

from cli.handlers import cmd_handler
from constants import CONSOLE
from db.command_history import save_command, load_history
from rich.console import Console as RichConsole

_RL_START = '\001'
_RL_END = '\002'

_rend = RichConsole(
    file=StringIO(), force_terminal=True, color_system='truecolor'
)


def _prompt(markup: str) -> str:
    _rend.file = StringIO()
    _rend.print(markup, end='')
    raw = _rend.file.getvalue()
    parts = re.split(r'(\x1b\[[0-9;]*[a-zA-Z])', raw)
    return ''.join(
        f'{_RL_START}{part}{_RL_END}' if part.startswith('\x1b[') else part
        for part in parts
    )


def render_title():
    CONSOLE.clear()
    CONSOLE.rule("[bold green]PU$H3R'S 2DO CLI", style='bold cyan')


def render_input_prompt():
    quit = False
    while not quit:
        cmd = input(_prompt('[bold green]➜ 2DO: '))
        save_command(cmd)
        quit = cmd_handler(cmd)


def startup():
    for cmd in load_history(100):
        readline.add_history(cmd)
    render_title()
    render_input_prompt()
