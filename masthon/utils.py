"""
Simple utils module.
"""

from typing import Any, Callable, Type

import traceback
import sys, select

DEBUG = False  # If debug is true errors are raised. Else they will be ignored (just printed).


def get_user_input():
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip()
    return None


def LOG(
    before: bool = False, after: bool = True, args_max_lenght: int = -1
) -> Callable:
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
                if args_max_lenght < 18:
                    print(
                        f"\033[1m\033[93m[LOG]\033[96m Called   |\033[0m  {func.__name__}(*args, **kwargs)"
                    )
                else:
                    argsnkwargs = (
                        ", ".join([repr(arg) for arg in args])
                        + ","
                        + ", ".join(
                            ["=".join((str(k), str(v))) for k, v in kwargs.items()]
                        )
                    )

                    print(
                        f"""\033[1m\033[93m[LOG]\033[96m Called   |\033[0m  {
                            func.__name__
                        }({
                            argsnkwargs[: (args_max_lenght // 2) - 3] + 
                            "..." + 
                            argsnkwargs[- args_max_lenght // 2 :]
                        })"""
                    )
            r = func(*args, **kwargs)
            if after:
                print(f"\033[1m\033[93m[LOG]\033[92m Returned |>\033[0m {r}")
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
                else:
                    traceback.print_exception(exc)
                    return None
            except Exception as e:
                traceback.print_exception(exc)
            else:
                return return_

        return _wrapper

    return _decorator
