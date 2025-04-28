"""
Just a submodule for all exceptions you can raise and catch specific errors related to Masthon.
"""


# All custom exceptions are childrens of this class
class MasthonException(BaseException): ...


# IO Transfer Errors
class IOTransferException(MasthonException, IOError): ...


# Web errors
class UnexpectedServerResult(IOTransferException): ...


class HTTPError(IOTransferException): ...


class HTTPRequestError400(HTTPError): ...


class HTTP401Error(HTTPRequestError400):...


class HTTPServerError500(HTTPError): ...


# Dataclass Exception(s)
class DataClassException(MasthonException): ...


# Class of CLI exceptions
class RealException(MasthonException): ...


class CLIException(MasthonException): ...


class CommandNotFound(CLIException): ...


class CommandExecutionError(CLIException, RuntimeError): ...
