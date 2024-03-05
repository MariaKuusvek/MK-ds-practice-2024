from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SuggestionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("book1id", "book1name", "book1author", "book2id", "book2name", "book2author")
    BOOK1ID_FIELD_NUMBER: _ClassVar[int]
    BOOK1NAME_FIELD_NUMBER: _ClassVar[int]
    BOOK1AUTHOR_FIELD_NUMBER: _ClassVar[int]
    BOOK2ID_FIELD_NUMBER: _ClassVar[int]
    BOOK2NAME_FIELD_NUMBER: _ClassVar[int]
    BOOK2AUTHOR_FIELD_NUMBER: _ClassVar[int]
    book1id: str
    book1name: str
    book1author: str
    book2id: str
    book2name: str
    book2author: str
    def __init__(self, book1id: _Optional[str] = ..., book1name: _Optional[str] = ..., book1author: _Optional[str] = ..., book2id: _Optional[str] = ..., book2name: _Optional[str] = ..., book2author: _Optional[str] = ...) -> None: ...
