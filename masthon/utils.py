"""
Simple utils module.
"""

from typing import Any, Callable

import traceback
import sys, select

DEBUG = True  # If debug is true errors are raised. Else they will be ignored.


def get_user_input():
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip()
    return None


def LOG(before: bool = False, after: bool = True) -> Callable:
    def _decorator(func: Callable) -> Callable:
        def _wrapper(*args, **kwargs) -> Any:
            if before:
                # print(
                #     f"\033[1m\033[93m[LOG]\033[96m Called   |\033[0m  {func.__name__}({', '.join([repr(arg) for arg in args])}, {', '.join(["=".join((k, v)) for k, v in kwargs.items()])})"
                # )
                print(
                    f"\033[1m\033[93m[LOG]\033[96m Called   |\033[0m  {func.__name__}(*args, **kwargs)"
                )
            r = func(*args, **kwargs)
            if after:
                print(f"\033[1m\033[93m[LOG]\033[92m Returned |>\033[0m {r}")
            return r

        return _wrapper

    return _decorator


def TRY(func: Callable):
    def _wrapper(*args, **kwargs) -> Any:
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            if DEBUG:
                raise e
            else:
                print(traceback.format_exc())
            return e
        else:
            return r

    return _wrapper


def OWTRY(overwrite_debug: bool = True) -> Callable:
    if overwrite_debug:

        def _decorator(func: Callable) -> Callable:
            def _wrapper(*args, **kwargs) -> Any:
                try:
                    r = func(*args, **kwargs)
                except Exception as e:
                    raise e
                else:
                    return r

            return _wrapper

    else:

        def _decorator(func: Callable) -> Callable:
            def _wrapper(*args, **kwargs) -> Any:
                try:
                    r = func(*args, **kwargs)
                except Exception as e:
                    print(traceback.format_exc())
                    return e
                else:
                    return r

            return _wrapper

    return _decorator


def get_user_input():
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip()
    return None
