import stimparam_pb2 as _stimparam_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Port(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    A: _ClassVar[Port]
    B: _ClassVar[Port]
    C: _ClassVar[Port]
    D: _ClassVar[Port]
A: Port
B: Port
C: Port
D: Port

class StatusReply(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: bool
    message: str
    def __init__(self, status: bool = ..., message: _Optional[str] = ...) -> None: ...

class SaveInfo(_message.Message):
    __slots__ = ("channels", "tag", "triggers")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[int]
    tag: str
    triggers: bool
    def __init__(self, channels: _Optional[_Iterable[int]] = ..., tag: _Optional[str] = ..., triggers: bool = ...) -> None: ...

class CoefThreshold(_message.Message):
    __slots__ = ("channel", "coef_threshold")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    COEF_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    channel: int
    coef_threshold: float
    def __init__(self, channel: _Optional[int] = ..., coef_threshold: _Optional[float] = ...) -> None: ...

class CoefThresholds(_message.Message):
    __slots__ = ("chan_threshold",)
    CHAN_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    chan_threshold: _containers.RepeatedCompositeFieldContainer[CoefThreshold]
    def __init__(self, chan_threshold: _Optional[_Iterable[_Union[CoefThreshold, _Mapping]]] = ...) -> None: ...

class TriggersInfo(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, tags: _Optional[_Iterable[int]] = ...) -> None: ...

class VarThreshold(_message.Message):
    __slots__ = ("channel", "update")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    channel: int
    update: bool
    def __init__(self, channel: _Optional[int] = ..., update: bool = ...) -> None: ...

class VarThresholds(_message.Message):
    __slots__ = ("update_chan",)
    UPDATE_CHAN_FIELD_NUMBER: _ClassVar[int]
    update_chan: _containers.RepeatedCompositeFieldContainer[VarThreshold]
    def __init__(self, update_chan: _Optional[_Iterable[_Union[VarThreshold, _Mapping]]] = ...) -> None: ...

class ExpName(_message.Message):
    __slots__ = ("port", "name")
    PORT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    port: Port
    name: str
    def __init__(self, port: _Optional[_Union[Port, str]] = ..., name: _Optional[str] = ...) -> None: ...

class ExpNames(_message.Message):
    __slots__ = ("update_expname",)
    UPDATE_EXPNAME_FIELD_NUMBER: _ClassVar[int]
    update_expname: _containers.RepeatedCompositeFieldContainer[ExpName]
    def __init__(self, update_expname: _Optional[_Iterable[_Union[ExpName, _Mapping]]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FloatArrayChunk(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, data: _Optional[_Iterable[float]] = ...) -> None: ...

class ChannelsArray(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, channels: _Optional[_Iterable[int]] = ...) -> None: ...

class DurationCount(_message.Message):
    __slots__ = ("time",)
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: int
    def __init__(self, time: _Optional[int] = ...) -> None: ...

class CountArray(_message.Message):
    __slots__ = ("counts",)
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    counts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, counts: _Optional[_Iterable[int]] = ...) -> None: ...

class DebugInfo(_message.Message):
    __slots__ = ("raw_queue", "loop_ms")
    RAW_QUEUE_FIELD_NUMBER: _ClassVar[int]
    LOOP_MS_FIELD_NUMBER: _ClassVar[int]
    raw_queue: float
    loop_ms: int
    def __init__(self, raw_queue: _Optional[float] = ..., loop_ms: _Optional[int] = ...) -> None: ...
