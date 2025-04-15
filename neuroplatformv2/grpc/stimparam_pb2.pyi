from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Shape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Biphasic: _ClassVar[Shape]
    BiphasicWithInterphaseDelay: _ClassVar[Shape]
    Triphasic: _ClassVar[Shape]

class Polarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NegativeFirst: _ClassVar[Polarity]
    PositiveFirst: _ClassVar[Polarity]

class TriggerEdgeOrLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Edge: _ClassVar[TriggerEdgeOrLevel]
    Level: _ClassVar[TriggerEdgeOrLevel]

class TriggerHighOrLow(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    High: _ClassVar[TriggerHighOrLow]
    Low: _ClassVar[TriggerHighOrLow]

class PulseOrTrain(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SinglePulse: _ClassVar[PulseOrTrain]
    PulseTrain: _ClassVar[PulseOrTrain]
Biphasic: Shape
BiphasicWithInterphaseDelay: Shape
Triphasic: Shape
NegativeFirst: Polarity
PositiveFirst: Polarity
Edge: TriggerEdgeOrLevel
Level: TriggerEdgeOrLevel
High: TriggerHighOrLow
Low: TriggerHighOrLow
SinglePulse: PulseOrTrain
PulseTrain: PulseOrTrain

class StimParam(_message.Message):
    __slots__ = ("channel", "shape", "polarity", "source", "triggeredgeorlevel", "triggerhighorlow", "pulse", "stimenabled", "maintainampsettle", "enableampsettle", "enablechargerecovery", "firstphasedurationmicroseconds", "secondphasedurationmicroseconds", "interphasedelaymicroseconds", "firstphaseamplitudemicroamps", "secondphaseamplitudemicroamps", "posttriggerdelaymicroseconds", "pulsetrainperiodmicroseconds", "refractoryperiodmicroseconds", "prestimampsettlemicroseconds", "poststimampsettlemicroseconds", "poststimchargerecovonmicroseconds", "poststimchargerecovoffmicroseconds", "numberofstimpulses")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    POLARITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TRIGGEREDGEORLEVEL_FIELD_NUMBER: _ClassVar[int]
    TRIGGERHIGHORLOW_FIELD_NUMBER: _ClassVar[int]
    PULSE_FIELD_NUMBER: _ClassVar[int]
    STIMENABLED_FIELD_NUMBER: _ClassVar[int]
    MAINTAINAMPSETTLE_FIELD_NUMBER: _ClassVar[int]
    ENABLEAMPSETTLE_FIELD_NUMBER: _ClassVar[int]
    ENABLECHARGERECOVERY_FIELD_NUMBER: _ClassVar[int]
    FIRSTPHASEDURATIONMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    SECONDPHASEDURATIONMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    INTERPHASEDELAYMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    FIRSTPHASEAMPLITUDEMICROAMPS_FIELD_NUMBER: _ClassVar[int]
    SECONDPHASEAMPLITUDEMICROAMPS_FIELD_NUMBER: _ClassVar[int]
    POSTTRIGGERDELAYMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    PULSETRAINPERIODMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    REFRACTORYPERIODMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    PRESTIMAMPSETTLEMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    POSTSTIMAMPSETTLEMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    POSTSTIMCHARGERECOVONMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    POSTSTIMCHARGERECOVOFFMICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFSTIMPULSES_FIELD_NUMBER: _ClassVar[int]
    channel: int
    shape: Shape
    polarity: Polarity
    source: int
    triggeredgeorlevel: TriggerEdgeOrLevel
    triggerhighorlow: TriggerHighOrLow
    pulse: PulseOrTrain
    stimenabled: bool
    maintainampsettle: bool
    enableampsettle: bool
    enablechargerecovery: bool
    firstphasedurationmicroseconds: float
    secondphasedurationmicroseconds: float
    interphasedelaymicroseconds: float
    firstphaseamplitudemicroamps: float
    secondphaseamplitudemicroamps: float
    posttriggerdelaymicroseconds: float
    pulsetrainperiodmicroseconds: float
    refractoryperiodmicroseconds: float
    prestimampsettlemicroseconds: float
    poststimampsettlemicroseconds: float
    poststimchargerecovonmicroseconds: float
    poststimchargerecovoffmicroseconds: float
    numberofstimpulses: int
    def __init__(self, channel: _Optional[int] = ..., shape: _Optional[_Union[Shape, str]] = ..., polarity: _Optional[_Union[Polarity, str]] = ..., source: _Optional[int] = ..., triggeredgeorlevel: _Optional[_Union[TriggerEdgeOrLevel, str]] = ..., triggerhighorlow: _Optional[_Union[TriggerHighOrLow, str]] = ..., pulse: _Optional[_Union[PulseOrTrain, str]] = ..., stimenabled: bool = ..., maintainampsettle: bool = ..., enableampsettle: bool = ..., enablechargerecovery: bool = ..., firstphasedurationmicroseconds: _Optional[float] = ..., secondphasedurationmicroseconds: _Optional[float] = ..., interphasedelaymicroseconds: _Optional[float] = ..., firstphaseamplitudemicroamps: _Optional[float] = ..., secondphaseamplitudemicroamps: _Optional[float] = ..., posttriggerdelaymicroseconds: _Optional[float] = ..., pulsetrainperiodmicroseconds: _Optional[float] = ..., refractoryperiodmicroseconds: _Optional[float] = ..., prestimampsettlemicroseconds: _Optional[float] = ..., poststimampsettlemicroseconds: _Optional[float] = ..., poststimchargerecovonmicroseconds: _Optional[float] = ..., poststimchargerecovoffmicroseconds: _Optional[float] = ..., numberofstimpulses: _Optional[int] = ...) -> None: ...
