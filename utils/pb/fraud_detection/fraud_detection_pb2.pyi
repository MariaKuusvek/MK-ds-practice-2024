from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FraudRequest(_message.Message):
    __slots__ = ("creditcardnr",)
    CREDITCARDNR_FIELD_NUMBER: _ClassVar[int]
    creditcardnr: str
    def __init__(self, creditcardnr: _Optional[str] = ...) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...
