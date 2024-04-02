from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutorRequest(_message.Message):
    __slots__ = ("var",)
    VAR_FIELD_NUMBER: _ClassVar[int]
    var: str
    def __init__(self, var: _Optional[str] = ...) -> None: ...

class ExecutorResponse(_message.Message):
    __slots__ = ("var2",)
    VAR2_FIELD_NUMBER: _ClassVar[int]
    var2: str
    def __init__(self, var2: _Optional[str] = ...) -> None: ...
