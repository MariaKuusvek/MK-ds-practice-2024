# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x05hello\"5\n\x13VerificationRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\x12\r\n\x05newVC\x18\x02 \x03(\x05\"\xee\x01\n\x19VerificationThreadRequest\x12\x13\n\x0bitemsLength\x18\x01 \x01(\x05\x12\x10\n\x08userName\x18\x02 \x01(\t\x12\x13\n\x0buserContact\x18\x03 \x01(\t\x12\x0e\n\x06street\x18\x04 \x01(\t\x12\x0c\n\x04\x63ity\x18\x05 \x01(\t\x12\r\n\x05state\x18\x06 \x01(\t\x12\x0b\n\x03zip\x18\x07 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x08 \x01(\t\x12\x14\n\x0c\x63reditcardnr\x18\t \x01(\t\x12\x0b\n\x03\x63vv\x18\n \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x0b \x01(\t\x12\x0f\n\x07orderId\x18\x0c \x01(\t\"\x1b\n\x19VerificationDeleteRequest\"\x1c\n\x1aVerificationDeleteResponse\"F\n\x14VerificationResponse\x12\x0f\n\x07verdict\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\r\n\x05\x62ooks\x18\x03 \x01(\t2\xf3\x02\n\x13VerificationService\x12Z\n\x19startTransVerMicroService\x12 .hello.VerificationThreadRequest\x1a\x1b.hello.VerificationResponse\x12K\n\x10\x63reditCardEventD\x12\x1a.hello.VerificationRequest\x1a\x1b.hello.VerificationResponse\x12`\n\x19\x64\x65leteDataInMicroservices\x12 .hello.VerificationDeleteRequest\x1a!.hello.VerificationDeleteResponse\x12Q\n\ndeleteData\x12 .hello.VerificationDeleteRequest\x1a!.hello.VerificationDeleteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VERIFICATIONREQUEST']._serialized_start=41
  _globals['_VERIFICATIONREQUEST']._serialized_end=94
  _globals['_VERIFICATIONTHREADREQUEST']._serialized_start=97
  _globals['_VERIFICATIONTHREADREQUEST']._serialized_end=335
  _globals['_VERIFICATIONDELETEREQUEST']._serialized_start=337
  _globals['_VERIFICATIONDELETEREQUEST']._serialized_end=364
  _globals['_VERIFICATIONDELETERESPONSE']._serialized_start=366
  _globals['_VERIFICATIONDELETERESPONSE']._serialized_end=394
  _globals['_VERIFICATIONRESPONSE']._serialized_start=396
  _globals['_VERIFICATIONRESPONSE']._serialized_end=466
  _globals['_VERIFICATIONSERVICE']._serialized_start=469
  _globals['_VERIFICATIONSERVICE']._serialized_end=840
# @@protoc_insertion_point(module_scope)
