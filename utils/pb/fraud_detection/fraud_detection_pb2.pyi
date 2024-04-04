from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FraudRequest(_message.Message):
    __slots__ = ("orderId", "newVC")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    NEWVC_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    newVC: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, orderId: _Optional[str] = ..., newVC: _Optional[_Iterable[int]] = ...) -> None: ...

class FraudThreadRequest(_message.Message):
    __slots__ = ("creditCardNr", "userName", "userContact")
    CREDITCARDNR_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USERCONTACT_FIELD_NUMBER: _ClassVar[int]
    creditCardNr: str
    userName: str
    userContact: str
    def __init__(self, creditCardNr: _Optional[str] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ...) -> None: ...

class FraudDeleteRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FraudDeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("verdict", "reason", "books")
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    reason: str
    books: str
    def __init__(self, verdict: _Optional[str] = ..., reason: _Optional[str] = ..., books: _Optional[str] = ...) -> None: ...
