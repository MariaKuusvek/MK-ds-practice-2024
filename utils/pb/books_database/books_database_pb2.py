# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: books_database.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x62ooks_database.proto\x12\x05hello\")\n\x13\x44\x61tabaseReadRequest\x12\x12\n\nbook_title\x18\x01 \x01(\t\"<\n\x14\x44\x61tabaseWriteRequest\x12\x12\n\nbook_title\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"(\n\x14\x44\x61tabaseReadResponse\x12\x10\n\x08quantity\x18\x01 \x01(\x05\"(\n\x15\x44\x61tabaseWriteResponse\x12\x0f\n\x07verdict\x18\x01 \x01(\t\"\x18\n\x16\x44\x61tabasePrepareRequest\"*\n\x17\x44\x61tabasePrepareResponse\x12\x0f\n\x07verdict\x18\x01 \x01(\t2\xf9\x01\n\x0f\x44\x61tabaseService\x12G\n\x0creadDatabase\x12\x1a.hello.DatabaseReadRequest\x1a\x1b.hello.DatabaseReadResponse\x12J\n\rwriteDatabase\x12\x1b.hello.DatabaseWriteRequest\x1a\x1c.hello.DatabaseWriteResponse\x12Q\n\x10prepareToExecute\x12\x1d.hello.DatabasePrepareRequest\x1a\x1e.hello.DatabasePrepareResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'books_database_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DATABASEREADREQUEST']._serialized_start=31
  _globals['_DATABASEREADREQUEST']._serialized_end=72
  _globals['_DATABASEWRITEREQUEST']._serialized_start=74
  _globals['_DATABASEWRITEREQUEST']._serialized_end=134
  _globals['_DATABASEREADRESPONSE']._serialized_start=136
  _globals['_DATABASEREADRESPONSE']._serialized_end=176
  _globals['_DATABASEWRITERESPONSE']._serialized_start=178
  _globals['_DATABASEWRITERESPONSE']._serialized_end=218
  _globals['_DATABASEPREPAREREQUEST']._serialized_start=220
  _globals['_DATABASEPREPAREREQUEST']._serialized_end=244
  _globals['_DATABASEPREPARERESPONSE']._serialized_start=246
  _globals['_DATABASEPREPARERESPONSE']._serialized_end=288
  _globals['_DATABASESERVICE']._serialized_start=291
  _globals['_DATABASESERVICE']._serialized_end=540
# @@protoc_insertion_point(module_scope)
