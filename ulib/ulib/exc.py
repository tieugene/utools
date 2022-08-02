"""Exceptions."""


class UlibError(RuntimeError):
    """Basic error"""
    ...


class UlibTextError(UlibError):
    """Exception with a text msg"""
    name: str
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return f"{self.name} error: {self.msg}"
