# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: JPGData.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='JPGData.proto',
  package='akproto1',
  syntax='proto3',
  serialized_pb=_b('\n\rJPGData.proto\x12\x08\x61kproto1\"\x83\x01\n\x07JPGData\x12\r\n\x05width\x18\x01 \x01(\r\x12\x0e\n\x06height\x18\x02 \x01(\r\x12\x19\n\x11\x63ompression_ratio\x18\x03 \x01(\r\x12\x12\n\ntotal_size\x18\x04 \x01(\r\x12\x16\n\x0e\x63olor_channels\x18\x05 \x01(\r\x12\x12\n\nimage_data\x18\x06 \x01(\x0c\x62\x06proto3')
)




_JPGDATA = _descriptor.Descriptor(
  name='JPGData',
  full_name='akproto1.JPGData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='akproto1.JPGData.width', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height', full_name='akproto1.JPGData.height', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='compression_ratio', full_name='akproto1.JPGData.compression_ratio', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_size', full_name='akproto1.JPGData.total_size', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='color_channels', full_name='akproto1.JPGData.color_channels', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_data', full_name='akproto1.JPGData.image_data', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=159,
)

DESCRIPTOR.message_types_by_name['JPGData'] = _JPGDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JPGData = _reflection.GeneratedProtocolMessageType('JPGData', (_message.Message,), dict(
  DESCRIPTOR = _JPGDATA,
  __module__ = 'JPGData_pb2'
  # @@protoc_insertion_point(class_scope:akproto1.JPGData)
  ))
_sym_db.RegisterMessage(JPGData)


# @@protoc_insertion_point(module_scope)
