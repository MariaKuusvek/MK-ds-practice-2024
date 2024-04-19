from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DatabaseReadRequest(_message.Message):
    __slots__ = ("book_title",)
    BOOK_TITLE_FIELD_NUMBER: _ClassVar[int]
    book_title: str
    def __init__(self, book_title: _Optional[str] = ...) -> None: ...

class DatabaseWriteRequest(_message.Message):
    __slots__ = ("book_title", "quantity")
    BOOK_TITLE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    book_title: str
    quantity: int
    def __init__(self, book_title: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class DatabaseReadResponse(_message.Message):
    __slots__ = ("quantity",)
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    def __init__(self, quantity: _Optional[int] = ...) -> None: ...

class DatabaseWriteResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...

class DatabasePrepareRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DatabasePrepareResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...
