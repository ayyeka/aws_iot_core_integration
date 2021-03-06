# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ChannelType.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ChannelType.proto',
  package='akproto1',
  syntax='proto3',
  serialized_pb=_b('\n\x11\x43hannelType.proto\x12\x08\x61kproto1*\xb7\x03\n\x0b\x43hannelType\x12\x19\n\x15\x41\x44\x43_4_20_CHANNEL_TYPE\x10\x00\x12\x18\n\x14\x41\x44\x43_0_5_CHANNEL_TYPE\x10\x01\x12\x15\n\x11PCNT_CHANNEL_TYPE\x10\x02\x12\x15\n\x11VBAT_CHANNEL_TYPE\x10\x03\x12\x15\n\x11TEMP_CHANNEL_TYPE\x10\x04\x12 \n\x1cHEALTH_COUNTERS_CHANNEL_TYPE\x10\x05\x12\x1b\n\x17GSM_SIGNAL_CHANNEL_TYPE\x10\x06\x12\x14\n\x10GPS_CHANNEL_TYPE\x10\x07\x12\x15\n\x11\x42LOB_CHANNEL_TYPE\x10\x08\x12\x15\n\x11GPIO_CHANNEL_TYPE\x10\t\x12\x1e\n\x1aMODBUS_UINT32_CHANNEL_TYPE\x10\n\x12\x1e\n\x1aMODBUS_SINT32_CHANNEL_TYPE\x10\x0b\x12\x1b\n\x17MODBUS_F32_CHANNEL_TYPE\x10\x0c\x12\x18\n\x14\x41\x44\x43_S32_CHANNEL_TYPE\x10\r\x12\x16\n\x12TOUCH_CHANNEL_TYPE\x10\x0e\x12\x1c\n\x18LORA_SIGNAL_CHANNEL_TYPE\x10\x0f\x62\x06proto3')
)

_CHANNELTYPE = _descriptor.EnumDescriptor(
  name='ChannelType',
  full_name='akproto1.ChannelType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ADC_4_20_CHANNEL_TYPE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADC_0_5_CHANNEL_TYPE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PCNT_CHANNEL_TYPE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VBAT_CHANNEL_TYPE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEMP_CHANNEL_TYPE', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HEALTH_COUNTERS_CHANNEL_TYPE', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GSM_SIGNAL_CHANNEL_TYPE', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GPS_CHANNEL_TYPE', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOB_CHANNEL_TYPE', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GPIO_CHANNEL_TYPE', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MODBUS_UINT32_CHANNEL_TYPE', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MODBUS_SINT32_CHANNEL_TYPE', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MODBUS_F32_CHANNEL_TYPE', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADC_S32_CHANNEL_TYPE', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOUCH_CHANNEL_TYPE', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LORA_SIGNAL_CHANNEL_TYPE', index=15, number=15,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=32,
  serialized_end=471,
)
_sym_db.RegisterEnumDescriptor(_CHANNELTYPE)

ChannelType = enum_type_wrapper.EnumTypeWrapper(_CHANNELTYPE)
ADC_4_20_CHANNEL_TYPE = 0
ADC_0_5_CHANNEL_TYPE = 1
PCNT_CHANNEL_TYPE = 2
VBAT_CHANNEL_TYPE = 3
TEMP_CHANNEL_TYPE = 4
HEALTH_COUNTERS_CHANNEL_TYPE = 5
GSM_SIGNAL_CHANNEL_TYPE = 6
GPS_CHANNEL_TYPE = 7
BLOB_CHANNEL_TYPE = 8
GPIO_CHANNEL_TYPE = 9
MODBUS_UINT32_CHANNEL_TYPE = 10
MODBUS_SINT32_CHANNEL_TYPE = 11
MODBUS_F32_CHANNEL_TYPE = 12
ADC_S32_CHANNEL_TYPE = 13
TOUCH_CHANNEL_TYPE = 14
LORA_SIGNAL_CHANNEL_TYPE = 15


DESCRIPTOR.enum_types_by_name['ChannelType'] = _CHANNELTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
