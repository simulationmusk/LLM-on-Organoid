from enum import Enum


class StimShape(Enum):
    """Stimulation Shape
    Biphasic
    BiphasicWithInterphaseDelay
    Triphasic
    """

    Biphasic = 0
    BiphasicWithInterphaseDelay = 1
    Triphasic = 3


class StimPolarity(Enum):
    """Start polarity of the stimulation"""

    NegativeFirst = 0
    PositiveFirst = 1


class PeristalticDirection(Enum):
    """Peristaltic pump direction"""

    CounterClockWise = 0
    ClockWise = 1


class MEA(Enum):
    """Mea Number"""

    One = 0
    Two = 1
    Three = 2
    Four = 3
    Five = 4
    Six = 5
    Seven = 6
    Eight = 7


class PumpId(Enum):
    One = 1
    Two = 2
    Three = 3
