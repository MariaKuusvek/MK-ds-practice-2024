from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SuggestionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("books",)
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    books: str
    def __init__(self, books: _Optional[str] = ...) -> None: ...
