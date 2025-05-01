Just some functions.


# `DEBUG`
#constant #exceptionManaging 
`bool` 
If debug is true errors are raised. Else they will be ignored (just printed). You can Change this value inside the file download if you want.
# `get_user_input(...)`
#function #CLI 
`def get_user_input() -> Optional[str]:`
Return a string if some `sys.stdin` available
# `LOG(...)`
#function #decoratorGenerator 
```py
def LOG(
    before: bool = False, after: bool = True, args_max_lenght: int = -1
) -> Callable:
```
Return a decorator who log your function (after or/and before). `args_max_lenght` is the length of the args's string to not crow you `stdout`.
# `TRY(...)`
#function #decoratorGenerator #exceptionManaging 
`def TRY(catched: Type[BaseException] = BaseException) -> Callable:`
Make your function catch errors of type specified.