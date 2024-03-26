from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationRequest(_message.Message):
    __slots__ = ("orderId", "newVC")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    NEWVC_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    newVC: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, orderId: _Optional[str] = ..., newVC: _Optional[_Iterable[int]] = ...) -> None: ...

class VerificationThreadRequest(_message.Message):
    __slots__ = ("itemsLength", "userName", "userContact", "street", "city", "state", "zip", "country", "creditcardnr", "cvv", "expirationDate")
    ITEMSLENGTH_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USERCONTACT_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CREDITCARDNR_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    itemsLength: int
    userName: str
    userContact: str
    street: str
    city: str
    state: str
    zip: str
    country: str
    creditcardnr: str
    cvv: str
    expirationDate: str
    def __init__(self, itemsLength: _Optional[int] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ..., creditcardnr: _Optional[str] = ..., cvv: _Optional[str] = ..., expirationDate: _Optional[str] = ...) -> None: ...

class VerificationResponse(_message.Message):
    __slots__ = ("verdict", "reason", "books")
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    reason: str
    books: str
    def __init__(self, verdict: _Optional[str] = ..., reason: _Optional[str] = ..., books: _Optional[str] = ...) -> None: ...
