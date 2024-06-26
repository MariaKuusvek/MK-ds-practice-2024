from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class QueueRequest(_message.Message):
    __slots__ = ("bookQuantity", "bookTitle", "userName", "userContact", "street", "city", "state", "zip", "country", "creditcardnr", "cvv", "expirationDate", "orderId")
    BOOKQUANTITY_FIELD_NUMBER: _ClassVar[int]
    BOOKTITLE_FIELD_NUMBER: _ClassVar[int]
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
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    bookQuantity: int
    bookTitle: str
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
    orderId: str
    def __init__(self, bookQuantity: _Optional[int] = ..., bookTitle: _Optional[str] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ..., creditcardnr: _Optional[str] = ..., cvv: _Optional[str] = ..., expirationDate: _Optional[str] = ..., orderId: _Optional[str] = ...) -> None: ...

class QueueRequestDequeue(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueueResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...

class QueueResponseDequeue(_message.Message):
    __slots__ = ("bookQuantity", "bookTitle", "userName", "userContact", "street", "city", "state", "zip", "country", "creditcardnr", "cvv", "expirationDate", "orderId")
    BOOKQUANTITY_FIELD_NUMBER: _ClassVar[int]
    BOOKTITLE_FIELD_NUMBER: _ClassVar[int]
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
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    bookQuantity: int
    bookTitle: str
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
    orderId: str
    def __init__(self, bookQuantity: _Optional[int] = ..., bookTitle: _Optional[str] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ..., creditcardnr: _Optional[str] = ..., cvv: _Optional[str] = ..., expirationDate: _Optional[str] = ..., orderId: _Optional[str] = ...) -> None: ...
