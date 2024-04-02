from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class QueueRequest(_message.Message):
    __slots__ = ("itemsLength", "userName", "userContact", "street", "city", "state", "zip", "country", "creditcardnr", "cvv", "expirationDate", "orderId")
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
    ORDERID_FIELD_NUMBER: _ClassVar[int]
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
    orderId: str
    def __init__(self, itemsLength: _Optional[int] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ..., creditcardnr: _Optional[str] = ..., cvv: _Optional[str] = ..., expirationDate: _Optional[str] = ..., orderId: _Optional[str] = ...) -> None: ...

class QueueRequestDequeue(_message.Message):
    __slots__ = ("orderId",)
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    def __init__(self, orderId: _Optional[str] = ...) -> None: ...

class QueueResponse(_message.Message):
    __slots__ = ("verdict",)
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    verdict: str
    def __init__(self, verdict: _Optional[str] = ...) -> None: ...
