# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import stimparam_pb2 as stimparam__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tapi.proto\x12\x03\x61pi\x1a\x0fstimparam.proto\"?\n\x0bStatusReply\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x14\n\x07message\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_message\";\n\x08SaveInfo\x12\x10\n\x08\x63hannels\x18\x01 \x03(\r\x12\x0b\n\x03tag\x18\x02 \x01(\t\x12\x10\n\x08triggers\x18\x03 \x01(\x08\"8\n\rCoefThreshold\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\r\x12\x16\n\x0e\x63oef_threshold\x18\x02 \x01(\x02\"<\n\x0e\x43oefThresholds\x12*\n\x0e\x63han_threshold\x18\x01 \x03(\x0b\x32\x12.api.CoefThreshold\"\x1c\n\x0cTriggersInfo\x12\x0c\n\x04tags\x18\x01 \x03(\r\"/\n\x0cVarThreshold\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\r\x12\x0e\n\x06update\x18\x02 \x01(\x08\"7\n\rVarThresholds\x12&\n\x0bupdate_chan\x18\x01 \x03(\x0b\x32\x11.api.VarThreshold\"0\n\x07\x45xpName\x12\x17\n\x04port\x18\x01 \x01(\x0e\x32\t.api.Port\x12\x0c\n\x04name\x18\x02 \x01(\t\"0\n\x08\x45xpNames\x12$\n\x0eupdate_expname\x18\x01 \x03(\x0b\x32\x0c.api.ExpName\"\x07\n\x05\x45mpty\"\x1f\n\x0f\x46loatArrayChunk\x12\x0c\n\x04\x64\x61ta\x18\x01 \x03(\x02\"!\n\rChannelsArray\x12\x10\n\x08\x63hannels\x18\x01 \x03(\r\"\x1d\n\rDurationCount\x12\x0c\n\x04time\x18\x01 \x01(\r\"\x1c\n\nCountArray\x12\x0e\n\x06\x63ounts\x18\x01 \x03(\r\"/\n\tDebugInfo\x12\x11\n\traw_queue\x18\x01 \x01(\x02\x12\x0f\n\x07loop_ms\x18\x02 \x01(\r*\"\n\x04Port\x12\x05\n\x01\x41\x10\x00\x12\x05\n\x01\x42\x10\x01\x12\x05\n\x01\x43\x10\x02\x12\x05\n\x01\x44\x10\x03\x32\x85\x05\n\x0cIntanService\x12%\n\x05start\x12\n.api.Empty\x1a\x10.api.StatusReply\x12$\n\x04stop\x12\n.api.Empty\x1a\x10.api.StatusReply\x12\x31\n\x0estartrecording\x12\r.api.SaveInfo\x1a\x10.api.StatusReply\x12-\n\rstoprecording\x12\n.api.Empty\x1a\x10.api.StatusReply\x12\x37\n\x0e\x63oefthresholds\x12\x13.api.CoefThresholds\x1a\x10.api.StatusReply\x12\x32\n\x0btriggertags\x12\x11.api.TriggersInfo\x1a\x10.api.StatusReply\x12\x34\n\x0cvarthreshold\x12\x12.api.VarThresholds\x1a\x10.api.StatusReply\x12*\n\x07\x65xpname\x12\r.api.ExpNames\x1a\x10.api.StatusReply\x12\x38\n\nstreamhaar\x12\x12.api.ChannelsArray\x1a\x14.api.FloatArrayChunk0\x01\x12-\n\tstimparam\x12\x0e.api.StimParam\x1a\x10.api.StatusReply\x12\x37\n\x0fupdatestimparam\x12\x12.api.ChannelsArray\x1a\x10.api.StatusReply\x12,\n\x05\x63ount\x12\x12.api.DurationCount\x1a\x0f.api.CountArray\x12\'\n\tdebuginfo\x12\n.api.Empty\x1a\x0e.api.DebugInfob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PORT']._serialized_start=704
  _globals['_PORT']._serialized_end=738
  _globals['_STATUSREPLY']._serialized_start=35
  _globals['_STATUSREPLY']._serialized_end=98
  _globals['_SAVEINFO']._serialized_start=100
  _globals['_SAVEINFO']._serialized_end=159
  _globals['_COEFTHRESHOLD']._serialized_start=161
  _globals['_COEFTHRESHOLD']._serialized_end=217
  _globals['_COEFTHRESHOLDS']._serialized_start=219
  _globals['_COEFTHRESHOLDS']._serialized_end=279
  _globals['_TRIGGERSINFO']._serialized_start=281
  _globals['_TRIGGERSINFO']._serialized_end=309
  _globals['_VARTHRESHOLD']._serialized_start=311
  _globals['_VARTHRESHOLD']._serialized_end=358
  _globals['_VARTHRESHOLDS']._serialized_start=360
  _globals['_VARTHRESHOLDS']._serialized_end=415
  _globals['_EXPNAME']._serialized_start=417
  _globals['_EXPNAME']._serialized_end=465
  _globals['_EXPNAMES']._serialized_start=467
  _globals['_EXPNAMES']._serialized_end=515
  _globals['_EMPTY']._serialized_start=517
  _globals['_EMPTY']._serialized_end=524
  _globals['_FLOATARRAYCHUNK']._serialized_start=526
  _globals['_FLOATARRAYCHUNK']._serialized_end=557
  _globals['_CHANNELSARRAY']._serialized_start=559
  _globals['_CHANNELSARRAY']._serialized_end=592
  _globals['_DURATIONCOUNT']._serialized_start=594
  _globals['_DURATIONCOUNT']._serialized_end=623
  _globals['_COUNTARRAY']._serialized_start=625
  _globals['_COUNTARRAY']._serialized_end=653
  _globals['_DEBUGINFO']._serialized_start=655
  _globals['_DEBUGINFO']._serialized_end=702
  _globals['_INTANSERVICE']._serialized_start=741
  _globals['_INTANSERVICE']._serialized_end=1386
# @@protoc_insertion_point(module_scope)
