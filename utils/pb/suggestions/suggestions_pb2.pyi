from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SuggestionsRequest(_message.Message):
    __slots__ = ("orderId", "newVC")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    NEWVC_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    newVC: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, orderId: _Optional[str] = ..., newVC: _Optional[_Iterable[int]] = ...) -> None: ...

class SuggestionsThreadRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuggestionsDeleteRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuggestionsDeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("verdict", "reason", "books")
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    reason: str
    books: str
    def __init__(self, verdict: _Optional[str] = ..., reason: _Optional[str] = ..., books: _Optional[str] = ...) -> None: ...
