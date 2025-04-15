from datetime import datetime
from typing import Any, Dict, List, Union

import numpy as np
from pydantic import BaseModel, Field, ConfigDict

from ..grpc.stimparam_pb2 import (
    StimParam as StimParamG,
    Shape,
    Polarity,
    TriggerEdgeOrLevel,
    TriggerHighOrLow,
    PulseOrTrain,
)
from .enumerations import MEA, PeristalticDirection, PumpId, StimPolarity, StimShape


class TriggerPattern(BaseModel):
    pattern: list[int] = Field(
        ...,
        description="List of 16 integers representing the trigger pattern.",
        min_items=16,
        max_items=16,
        example=[0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255],
    )


class ChannelVarThreshold(BaseModel):
    """Channel Variable Threshold enable/disable"""

    index: int = Field(default=0, description="Electrode index [0-127]", ge=0, le=127)
    enable: bool = Field(
        default=True, description="Enabled the variable threshold: 0 = false, 1 = true"
    )


class ChannelCoefThreshold(BaseModel):
    """Channel Coefficient multiplier std for Threshold"""

    index: int = Field(default=0, description="Electrode index [0-127]", ge=0, le=127)
    coef: float = Field(
        default=6.0, ge=0, description="Coefficient multiplier std for threshold"
    )


class StimParam(BaseModel):
    """Stimulation Parameter for one electrode"""

    index: int = Field(default=0, description="Electrode index [0-127]", ge=0, le=127)
    enable: bool = Field(
        default=True, description="Enabled the stimulation: 0 = false, 1 = true"
    )
    trigger_key: int = Field(
        default=0,
        description="Trigger key: [0-15] digital in connected to the trigger generator [0,15]",
        ge=0,
        le=15,
    )
    trigger_delay: int = Field(
        default=0, description="Post trigger delay [us]", ge=0, le=500000
    )
    nb_pulse: int = Field(
        default=0,
        description="Nb Stim pulse: 0: Single pulse, 1 and more: Pulse train",
        ge=0,
        le=256,
    )
    pulse_train_period: int = Field(
        default=10000, description="Pulse Train Period [us]", ge=0, le=1000000
    )
    post_stim_ref_period: float = Field(
        default=1000.0, description="Post-Stim Refractory Period [us]", ge=0, le=1000000
    )
    stim_shape: StimShape = Field(
        default=StimShape.Biphasic,
        description="Stimulation Shape: Biphasic, BiphasicWithInterphaseDelay, Triphasic",
    )
    polarity: StimPolarity = Field(
        default=StimPolarity.NegativeFirst,
        description="Start polarity of the stimulation: NegativeFirst, PositiveFirst",
    )
    phase_duration1: float = Field(default=100.0, description="D1 [us]", ge=0, le=5000)
    phase_duration2: float = Field(default=100.0, description="D2 [us]", ge=0, le=5000)
    phase_amplitude1: float = Field(default=1.0, description="A1 [uA]", ge=0)
    phase_amplitude2: float = Field(default=1.0, description="A2 [uA]", ge=0)
    enable_amp_settle: bool = Field(
        default=True, description="enable amp settle: 0 = false, 1 = true"
    )
    pre_stim_amp_settle: float = Field(
        default=0.0, description="Pre stim amp settle [us]", ge=0
    )
    post_stim_amp_settle: float = Field(
        default=1000.0, description="Post stim amp settle [us]", ge=0
    )
    enable_charge_recovery: bool = Field(
        default=True, description="enable charge recovery: 0 = false, 1 = true"
    )
    post_charge_recovery_on: float = Field(
        default=0.0, description="Post charge recovery on [us]", ge=0
    )
    post_charge_recovery_off: float = Field(
        default=100.0, description="Post charge recovery off [us]", ge=0
    )
    interphase_delay: float = Field(
        default=0.0,
        description="Interphase delay (for BiphasicWithInterphaseDelay) [us]",
        ge=0,
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._changes = {}
        for name, field in self.model_fields.items():
            value = data.get(name, field.default)
            self._changes[name] = value

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.model_fields:
            current_value = getattr(self, name, None)
            if current_value != value:
                self._changes[name] = value
        super().__setattr__(name, value)

    def _get_changes(self) -> Dict[str, Dict[str, Any]]:
        changes = self._changes.copy()
        self._changes.clear()
        return changes

    def to_grpc(self) -> StimParamG:
        changes = self._get_changes()
        stimparam_kwargs = {"channel": self.index}

        # Map the changes to the StimParam fields
        field_mapping = {
            "index": "channel",
            "stim_shape": "shape",
            "enable": "stimenabled",
            "polarity": "polarity",
            "phase_duration1": "firstphasedurationmicroseconds",
            "phase_duration2": "secondphasedurationmicroseconds",
            "phase_amplitude1": "firstphaseamplitudemicroamps",
            "phase_amplitude2": "secondphaseamplitudemicroamps",
            "trigger_key": "source",
            "trigger_delay": "posttriggerdelaymicroseconds",
            "nb_pulse": "pulse",
            "pulse_train_period": "pulsetrainperiodmicroseconds",
            "post_stim_ref_period": "refractoryperiodmicroseconds",
            "enable_amp_settle": "enableampsettle",
            "pre_stim_amp_settle": "prestimampsettlemicroseconds",
            "post_stim_amp_settle": "poststimampsettlemicroseconds",
            "enable_charge_recovery": "enablechargerecovery",
            "post_charge_recovery_on": "poststimchargerecovonmicroseconds",
            "post_charge_recovery_off": "poststimchargerecovoffmicroseconds",
            "interphase_delay": "interphasedelaymicroseconds",
        }

        for key, value in changes.items():
            if key in field_mapping:
                if key == "stim_shape":
                    # Mapping from StimShape to Shape
                    shape_mapping = {
                        StimShape.Biphasic: Shape.Biphasic,
                        StimShape.BiphasicWithInterphaseDelay: Shape.BiphasicWithInterphaseDelay,
                        StimShape.Triphasic: Shape.Triphasic,
                    }
                    stimparam_kwargs[field_mapping[key]] = shape_mapping[value]
                elif key == "polarity":
                    # Mapping from StimPolarity to Polarity
                    polarity_mapping = {
                        StimPolarity.NegativeFirst: Polarity.NegativeFirst,
                        StimPolarity.PositiveFirst: Polarity.PositiveFirst,
                    }
                    stimparam_kwargs[field_mapping[key]] = polarity_mapping[value]
                elif key == "trigger_edge_or_level":
                    # Mapping from TriggerEdgeOrLevel to TriggerEdgeOrLevel
                    edge_or_level_mapping = {
                        TriggerEdgeOrLevel.Edge: TriggerEdgeOrLevel.Edge,
                        TriggerEdgeOrLevel.Level: TriggerEdgeOrLevel.Level,
                    }
                    stimparam_kwargs[field_mapping[key]] = edge_or_level_mapping[value]
                elif key == "trigger_high_or_low":
                    # Mapping from TriggerHighOrLow to TriggerHighOrLow
                    high_or_low_mapping = {
                        TriggerHighOrLow.High: TriggerHighOrLow.High,
                        TriggerHighOrLow.Low: TriggerHighOrLow.Low,
                    }
                    stimparam_kwargs[field_mapping[key]] = high_or_low_mapping[value]
                elif key == "nb_pulse":
                    if value > 1:
                        stimparam_kwargs["pulse"] = PulseOrTrain.PulseTrain
                    else:
                        stimparam_kwargs["pulse"] = PulseOrTrain.SinglePulse
                    stimparam_kwargs["numberofstimpulses"] = value
                else:
                    stimparam_kwargs[field_mapping[key]] = value

        stimparam = StimParamG(**stimparam_kwargs)

        return stimparam

    def to_array(self):
        """Get stim parameter array for intan software
        :rtype: np.array
        """
        stimparm = np.empty(20, np.dtype("float32"))
        stimparm[0] = self.index
        stimparm[1] = self.enable
        stimparm[2] = self.trigger_key + 10.0
        stimparm[3] = self.trigger_delay
        stimparm[4] = self.nb_pulse
        stimparm[5] = self.pulse_train_period
        stimparm[6] = self.post_stim_ref_period
        stimparm[7] = self.stim_shape.value
        stimparm[8] = self.polarity.value
        stimparm[9] = self.phase_duration1
        stimparm[10] = self.phase_duration2
        stimparm[11] = self.phase_amplitude1
        stimparm[12] = self.phase_amplitude2
        stimparm[13] = self.enable_amp_settle
        stimparm[14] = self.pre_stim_amp_settle
        stimparm[15] = self.post_stim_amp_settle
        stimparm[16] = self.enable_charge_recovery
        stimparm[17] = self.post_charge_recovery_on
        stimparm[18] = self.post_charge_recovery_off
        stimparm[19] = self.interphase_delay
        return stimparm

    def display_attributes(self):
        attributes = [
            "index",
            "enable",
            "trigger_key",
            "trigger_delay",
            "nb_pulse",
            "pulse_train_period",
            "post_stim_ref_period",
            "stim_shape",
            "polarity",
            "phase_duration1",
            "phase_duration2",
            "phase_amplitude1",
            "phase_amplitude2",
            "enable_amp_settle",
            "pre_stim_amp_settle",
            "post_stim_amp_settle",
            "enable_charge_recovery",
            "post_charge_recovery_on",
            "post_charge_recovery_off",
            "interphase_delay",
        ]
        for attr in attributes:
            if hasattr(self, attr):
                print(f"{attr}: {getattr(self, attr)}")


class VarThresholdRequest(BaseModel):
    """Request model for enabling/disabling auto variation threshold."""

    channels: List[ChannelVarThreshold] = Field(
        ..., description="Send a list of channel variable threshold to intan software"
    )


class CoefThresholdRequest(BaseModel):
    """Request model for changing coef std for threshold."""

    channels: List[ChannelCoefThreshold] = Field(
        ..., description="Send a list of channel coef threshold to intan software"
    )


class CountListenerRequest(BaseModel):
    """Request model for setting count listener on selected triggers."""

    triggers: List[int] = Field(..., description="Selected triggers to listen")


class ReadCountResponse(BaseModel):
    """Response model for getting the number of spikes (of all electrodes) after selected triggers."""

    spike_counts: List[int] = Field(
        ..., description="Number of spike (of all electrodes) after triggers selected"
    )


class SetTagTriggerRequest(BaseModel):
    """Request model for setting tag to trigger."""

    tag: int = Field(
        ...,
        description="Set tag to trigger. It will be store in the database with all triggers",
    )


class StimParamRequest(BaseModel):
    """Send a list of stim parameter to intan software"""

    params: List[StimParam] = Field(
        ..., description="List of stim parameter for intan software"
    )


class UploadStimParamRequest(BaseModel):
    """Ask intan software to send the stim parameters to the headstage"""

    electrodes: List[int] = Field(..., description="List of electrodes")


class CountDurationRequest(BaseModel):
    """Ask Intan the number of spike for the duration"""

    duration: int = Field(default=100, description="Duration [ms]", ge=1, le=30000)


class CountDurationResponse(BaseModel):
    """Response model for getting the number of spikes (of all electrodes) for a selected duration."""

    spike_counts: List[int] = Field(
        ..., description="Number of spike (of all electrodes) for the selected duration"
    )


class StartRawRecordingRequest(BaseModel):
    """Start raw recording with the selected channels"""

    channels: List[int] = Field(
        ...,
        description="Start raw recording with the selected channels",
    )
    tag: str = Field(
        ...,
        description="File name tag",
    )
    triggers: bool = Field(..., description="Add triggers")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class TriggerUVSendRequest(BaseModel):
    """Model for representing the data sent in the send request"""

    t: int = Field(..., description="Activation period t of the UV", ge=1)


class SpikeEventQuery(BaseModel):
    start: datetime = Field(..., description="Start datetime for querying spike events")
    stop: datetime = Field(..., description="Stop datetime for querying spike events")
    fsname: str = Field(..., description="Name of the filesystem")


class RawSpikeQuery(BaseModel):
    start: datetime = Field(
        ..., description="Start datetime for querying raw spike events"
    )
    stop: datetime = Field(
        ..., description="Stop datetime for querying raw spike events"
    )
    index: int = Field(..., description="Index of the spike event")


class SpikeCountQuery(BaseModel):
    start: datetime = Field(..., description="Start datetime for querying spike counts")
    stop: datetime = Field(..., description="Stop datetime for querying spike counts")
    fsname: str = Field(..., description="Name of the filesystem")


class TriggersQuery(BaseModel):
    start: datetime = Field(..., description="Start datetime for querying triggers")
    stop: datetime = Field(..., description="Stop datetime for querying triggers")


class PeristalticState(BaseModel):
    rpm: float = Field(
        ...,
        description="The RPM (Revolutions Per Minute) value of the peristaltic pump.",
    )
    running: bool = Field(
        ...,
        description="The state of the peristaltic pump (True for running, False for stopped).",
    )
    direction: PeristalticDirection = Field(
        ..., description="The direction of rotation of the peristaltic pump."
    )
    prime: bool = Field(
        ...,
        description="The priming state of the peristaltic pump (True for primed, False for unprimed).",
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PeristalticState":
        """
        Creates a PeristalticState instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing pump state data.

        Returns:
            PeristalticState: An instance of PeristalticState initialized with the dictionary values.
        """
        direction = PeristalticDirection(data.get("direction"))
        return cls(
            rpm=data.get("rpm"),
            running=data.get("running"),
            direction=direction,
            prime=data.get("prime"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the PeristalticState instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the PeristalticState instance.
        """
        return {
            "rpm": self.rpm,
            "running": self.running,
            "direction": self.direction.value,
            "prime": self.prime,
        }

    def __repr__(self) -> str:
        return f"PeristalticState(rpm={self.rpm}, running={self.running}, direction={self.direction}, prime={self.prime})"


class PeristalticRequest(BaseModel):
    pump_id: PumpId = Field(
        ...,
        description="Id of the pump to be selected from the set {1,2,3}",
        ge=1,
        le=3,
    )


class PeristalticRpmRequest(BaseModel):
    speed: float = Field(..., description="speed")
    direction: PeristalticDirection = Field(
        ...,
        description="PeristalticDirection 0=CounterClockWise, 1=ClockWise",
        ge=0,
        le=1,
    )
    pump_id: PumpId = Field(
        ...,
        description="Id of the pump to be selected from the set {1,2,3}",
        ge=1,
        le=3,
    )


class ExperimentRequest(BaseModel):
    token: str = Field(
        ..., description="The unique token string identifying the experiment."
    )


class ExperimentStimParamRequest(BaseModel):
    token: str = Field(
        ..., description="The unique token string identifying the experiment."
    )
    index_electrode: int = Field(..., description="Index electrode.")


class CameraFromRequest(BaseModel):
    mea: MEA = Field(..., description="Mea Number")
    img_id: str = Field(..., description="Id of the image")


class CameraListImagesRequest(BaseModel):
    mea: MEA = Field(..., description="Mea Number")
    start_date: Union[str, datetime] = Field(
        ..., description="Start date of the interval for listing images taken"
    )
    end_date: Union[str, datetime] = Field(
        ..., description="End date of the interval for listing images taken"
    )


class CameraCaptureRequest(BaseModel):
    mea: MEA = Field(..., description="Mea Number")
