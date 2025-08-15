"""
Simple utils module.
"""

from typing import Any, Callable, Type, Optional, Iterable

from threading import Thread
from .log import logger
import format

from enum import Enum
import traceback


import sys, tty, termios, select


DEBUG = False  # If debug is true errors are raised. Else they will be ignored (just printed).



###### Modified

class ExceptionDesignedThread(Thread):
    def __init__(self, target: Callable[..., Any], args:tuple = tuple(), kwargs:dict = dict()) -> None:
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._exception = None
    
    @property
    def exception(self):
        return self._exception
    
    def run(self):
        try:
            self._target(*args, **kwargs)
        except BaseException as e:
            self._exception = e





fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)


line_input: str = ""
index: int = 0


hist: list[str] = list()
hindex: int = 0


def read1(io):
    if select.select([io], [], [], 0.005)[0]:
        return sys.stdin.read(1)
    return None


def init_line():
    global line_input, index
    line_input = ""
    index = 0


init_line()


def display(i: str) -> str:
    def cursor():
        c = index
        if c == len(i):
            return (
                i + format.FORMAT.REVERSE_BGFG + " " + format.FORMAT.RESET_REVERSE_BGFG
            )
        if len(i) > 1:
            return (
                i[:c]
                + format.FORMAT.REVERSE_BGFG
                + i[c]
                + format.FORMAT.RESET_REVERSE_BGFG
                + i[c + 1 :]
            )
        else:
            return (
                i + format.FORMAT.REVERSE_BGFG + " " + format.FORMAT.RESET_REVERSE_BGFG
            )

    i = cursor()
    s = i.split()
    return (
        format.FORMAT.FG.CYAN + s[0] + format.FORMAT.FG.RESET + " ".join([""] + s[1:])
    )


def get_user_input():
    tty.setraw(sys.stdin)
    sys.stdout.write("\033[s")  # save pos
    sys.stdout.flush()
    global line_input, index, hindex

    char = read1(sys.stdin)  # read one char and get char code
    if char is None:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return
    char = ord(char)

    # Manage internal data-model
    if char in {3, 4}:  # CTRL-C / CTRL-D
        sys.stdout.write("\033[1000D")  # Move all the way left
        sys.stdout.write("\033[1000B")  # Move all the way down
        sys.stdout.write("\033[0K")  # Clear the line
        sys.stdout.write("\033[u")
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return
        # raise EOFError("stdin cuted")
    elif char == 24:  # Cancel input
        line_input = ""
        index = 0
    elif char == 12:
        sys.stdout.write("\033[1000D")  # Move all the way left
        sys.stdout.write("\033[1000B")  # Move all the way down
        sys.stdout.write("\033[0K")  # Clear the line
        sys.stdout.write("\033[u")
        sys.stdout.write("\n" * 20 + "\033[20F")
        sys.stdout.flush()
        return
    elif 32 <= char <= 126:
        line_input = line_input[:index] + chr(char) + line_input[index:]
        index += 1
    elif char in {10, 13}:
        sys.stdout.write("\033[1000D")
        li = line_input
        line_input = ""
        index = 0
        hist.append(line_input)
        hindex = 0
        sys.stdout.write("\033[1000D")  # Move all the way left
        sys.stdout.write("\033[1000B")  # Move all the way down
        sys.stdout.write("\033[0K")  # Clear the line
        sys.stdout.write(
            format.FORMAT.BOLD + ">>> " + display(line_input) + format.FORMAT.NO_BOLD
        )
        tty.setcbreak(sys.stdin)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.flush()
        sys.stdout.write("\033[u")  # restore pos
        logger.info("Command entered: ", input=li)
        return li
    elif char == 27:  # \xb1, ansi escape char
        next1, next2 = read1(sys.stdin), read1(sys.stdin)
        if None in (next1, next2):
            return
        next1, next2 = ord(next1), ord(next2)
        if next1 == 91:  # [
            if next2 == 68:  # D -> Left
                index = max(0, index - 1)
            elif next2 == 67:  # C -> Right
                index = min(len(line_input), index + 1)
            elif next2 == 65:  # A -> Up
                hindex += 1 if hindex < len(hist) - 1 else 0
                if hindex == -1:
                    line_input = ""
                else:
                    line_input = hist[hindex]
                hindex = 0
            elif next2 == 66:  # B -> Down
                hindex -= 1 if hindex >= 0 else 0
                if hindex == -1:
                    line_input = ""
                else:
                    line_input = hist[hindex]
                hindex = 0
    elif char == 127:  # Basck space
        if len(line_input) > 0:
            line_input = line_input[: index - 1] + line_input[index:]
            index -= 1
    else:
        logger.debug("Input: Unknown char", ord=char, char=chr(char))

    # Print current line_input-string
    sys.stdout.write("\033[1000D")  # Move all the way left
    sys.stdout.write("\033[1000B")  # Move all the way down
    sys.stdout.write("\033[0K")  # Clear the line
    sys.stdout.write(
        format.FORMAT.BOLD + ">>> " + display(line_input) + format.FORMAT.NO_BOLD
    )
    tty.setcbreak(sys.stdin)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.flush()
    sys.stdout.write("\033[u")  # restore pos


##### AHAHAAH

# def get_user_input() -> Optional[str]:
#     if select.select([sys.stdin], [], [], 0.0)[0]:
#         return sys.stdin.readline().strip()
#     return None


def add_url_parameters(url: str, **kwargs) -> str:
    r = (
        url
        + ("?" if len(kwargs) > 0 else "")
        + "&".join(
            [
                (
                    k + "=" + str(v)
                    if not isinstance(v, Iterable)
                    else "".join(
                        [
                            k
                            + "[]"
                            + "="
                            + (vv.value if isinstance(vv, Enum) else str(vv))
                            for vv in v
                        ]
                    )
                )
                for k, v in kwargs.items()
                if v != None
            ]
        )
    )
    return r


def LOG(before: bool = False, after: bool = True) -> Callable:
    """Decorator to log yours funcs

    Args:
        before (bool, optional): Log before ?. Defaults to False.
        after (bool, optional): Log after ?. Defaults to True.
        args_max_lenght (int, optional): Prevent from multiline prints. Defaults to -1.

    Returns:
        Callable: ...
    """

    def _decorator(func: Callable) -> Callable:
        def _wrapper(*args, **kwargs) -> Any:
            if before:
                logger.debug(
                    f"! Called {func.__module__}.{func.__name__}()",
                    args=args,
                    kwargs=kwargs,
                )
            r = func(*args, **kwargs)
            if after:
                logger.debug(
                    f"> {func.__module__}.{func.__name__}() returned ", return_value=r
                )
            return r

        return _wrapper

    return _decorator


def TRY(catched: Type[BaseException] = BaseException) -> Callable:
    """Make your functions catch errors of a type specified

    Args:
        catched (Type[BaseException], optional): ... Defaults to BaseException.

    Returns:
        Callable: ...
    """

    def _decorator(func: Callable):
        def _wrapper(*args, **kwargs) -> Any:
            try:
                return_ = func(*args, **kwargs)
            except catched as exc:
                if DEBUG:
                    raise exc

                traceback.print_exception(exc)
                if len(exc.args) >= 3:
                    return exc.args[2]
                raise exc
            return return_

        return _wrapper

    return _decorator


def DEPRECATED(func: Callable) -> Callable:
    def _wrapper(*args, **kwargs) -> Any:
        logger.warning(
            f"Deprecated use of function {func.__module__}.{func.__name__}()"
        )
        return func(*args, **kwargs)

    return _wrapper
