from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationRequest(_message.Message):
    __slots__ = ("itemsLength",)
    ITEMSLENGTH_FIELD_NUMBER: _ClassVar[int]
    itemsLength: int
    def __init__(self, itemsLength: _Optional[int] = ...) -> None: ...

class VerificationResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...
