import grpc
from grpc import RpcError
from typing import List

from ..utils.constants import (
    INTAN_SERVICE_IP,
    INTAN_SERVICE_PORT,
)
from ..utils.exceptions import IntanConnectionError
from ..utils.schemas import (
    CountDurationRequest,
    CountDurationResponse,
    StartRawRecordingRequest,
    StimParam,
    ChannelVarThreshold,
    ChannelCoefThreshold,
    VarThresholdRequest,
    CoefThresholdRequest,
    StimParamRequest,
    UploadStimParamRequest,
)

from ..grpc.api_pb2 import (
    DurationCount,
    VarThreshold,
    VarThresholds,
    CoefThreshold,
    CoefThresholds,
    StatusReply,
    ChannelsArray,
    CountArray,
    Empty,
    SaveInfo,
)
from ..grpc.api_pb2_grpc import IntanServiceStub


class IntanController:
    """Intan Software connection. Handle connection and can configure the software.
    Don't forget to close the session after each use
    """

    def __init__(self):
        try:
            self.channel = grpc.aio.insecure_channel(
                f"{INTAN_SERVICE_IP}:{INTAN_SERVICE_PORT}"
            )
        except RpcError as e:
            raise IntanConnectionError(f"Connection failed: {str(e)}")

    async def _close(self):
        """Close the connection"""
        if self.channel:
            await self.channel.close()
            self.channel = None

    async def _var_threshold(
        self, channels_enabled: List[ChannelVarThreshold]
    ) -> StatusReply:
        """Enable/disable auto variation threshold."""
        vt = []
        for chan in channels_enabled:
            vt.append(VarThreshold(channel=chan.index, update=chan.enable))
        vts = VarThresholds(update_chan=vt)
        stub = IntanServiceStub(self.channel)
        response = await stub.varthreshold(vts)
        if response.HasField("message"):
            status = StatusReply(status=response.status, message=response.message)
        else:
            status = StatusReply(status=response.status, message=None)
        return status

    @classmethod
    async def var_threshold(cls, req: VarThresholdRequest) -> str:
        controller = cls()
        try:
            status = await controller._var_threshold(req.channels)
            return (
                "Auto variation threshold updated"
                + ("" if status.status else "not")
                + " successfully"
            )
        finally:
            await controller._close()

    async def _coef_threshold(
        self, channels_coef: List[ChannelCoefThreshold]
    ) -> StatusReply:
        """Change coef std threshold."""
        vt = []
        for chan in channels_coef:
            vt.append(CoefThreshold(channel=chan.index, coef_threshold=chan.coef))
        vts = CoefThresholds(chan_threshold=vt)
        stub = IntanServiceStub(self.channel)
        response = await stub.coefthresholds(vts)
        if response.HasField("message"):
            status = StatusReply(status=response.status, message=response.message)
        else:
            status = StatusReply(status=response.status, message=None)
        return status

    @classmethod
    async def coef_threshold(cls, req: CoefThresholdRequest) -> str:
        controller = cls()
        try:
            status = await controller._coef_threshold(req.channels)
            return (
                "Coef threshold updated"
                + ("" if status.status else "not")
                + " successfully"
            )
        finally:
            await controller._close()

    # async def _impedance(self):
    #     """Run impedance measurement"""
    #     run_impedance = np.empty(1, np.dtype("byte"))
    #     run_impedance[0] = 14
    #     run_impedance = run_impedance.tobytes()
    #     await self._send(run_impedance, 10)

    # @classmethod
    # async def impedance(cls) -> str:
    #     controller = cls()
    #     try:
    #         await controller._impedance()
    #         return "Impedance measurement run successfully"
    #     finally:
    #         controller._close()

    # async def _set_count(self, triggers: np.array):
    #     """
    #     Set count listener on selected triggers
    #     :type triggers: np.array
    #         Selected triggers to listen
    #     """
    #     data = np.empty(2 + len(triggers), np.dtype("byte"))
    #     data[0] = 15
    #     data[1] = len(triggers)
    #     data[2:] = triggers
    #     data = data.tobytes()
    #     await self._send(data, 2)

    # @classmethod
    # async def set_count(cls, req: CountListenerRequest) -> str:
    #     controller = cls()
    #     try:
    #         await controller._set_count(req.triggers)
    #         return "Set count listener on selected triggers successfully"
    #     finally:
    #         controller._close()

    # async def _read_count(self) -> np.array:
    #     """
    #     Get the number of spike (of all electrodes) after triggers selected
    #     :rtype: np.array
    #     """
    #     try:
    #         buffer = self.sock.recv(4 * 130)
    #         np_buffer = np.frombuffer(buffer, dtype=np.int32)
    #         return np_buffer[0:128]
    #     except socket.error:
    #         return np.array([])

    # @classmethod
    # async def read_count(cls) -> ReadCountResponse:
    #     controller = cls()
    #     try:
    #         return controller._read_count()
    #     finally:
    #         controller._close()

    # async def _set_tag_trigger(self, tag: int):
    #     """
    #     Set tag to trigger. It will be store in the database with all triggers
    #     :type tag: int
    #     """
    #     data = np.empty(2, np.dtype("byte"))
    #     data[0] = 16
    #     data[1] = tag
    #     data = data.tobytes()
    #     await self._send(data, 2)

    # @classmethod
    # async def set_tag_trigger(cls, req: SetTagTriggerRequest) -> str:
    #     controller = cls()
    #     try:
    #         await controller._set_tag_trigger(req.tag)
    #         return "Set tag to trigger successfully"
    #     finally:
    #         controller._close()

    async def _count_spike(self, duration: int) -> List[int]:
        """Count the number of spike during the interval
        :type duration: int
        """
        stub = IntanServiceStub(self.channel)
        dur = DurationCount()
        dur.time = duration
        resp: CountArray = await stub.count(dur)

        return resp.counts

    @classmethod
    async def count_spike(cls, req: CountDurationRequest) -> CountDurationResponse:
        controller = cls()
        try:
            return await controller._count_spike(req.duration)
        finally:
            await controller._close()

    async def _upload_stimparam(self, electrodes: List[int] = None) -> StatusReply:
        """Upload the stim parameter to the headstage. Must stop the board to upload the parameter.
        If no electrode specify, send all parameters (slower). If you specify few electrodes, the upload is faster.
        :type electrodes: List[int], optional
        """
        stub = IntanServiceStub(self.channel)
        status = StatusReply(status=True, message=None)

        if electrodes is None:
            channels = ChannelsArray(channels=[])
        else:
            channels = ChannelsArray(channels=electrodes)
        resp = await stub.updatestimparam(channels)
        if not resp.status:
            status.status = False
            status.message = resp.message
        return status

    @classmethod
    async def upload_stimparam(cls, req: UploadStimParamRequest) -> None:
        controller = cls()
        try:
            await controller._upload_stimparam(req.electrodes)
        finally:
            await controller._close()

    async def _send_stimparam(self, params: List[StimParam]) -> StatusReply:
        """Send a list of stim parameter to intan software
        :type param: List[StimParam]
        """
        stub = IntanServiceStub(self.channel)
        status = StatusReply(status=True, message=None)
        for param in params:
            sp = param.to_grpc()
            resp = await stub.stimparam(sp)
            if not resp.status:
                status.status = False
                if status.message:
                    status.message += f"; {resp.message}"
                else:
                    status.message = resp.message
        return status

    @classmethod
    async def send_stimparam(cls, req: StimParamRequest) -> None:
        controller = cls()
        try:
            await controller._send_stimparam(req.params)
        finally:
            await controller._close()

    async def _start_raw_recording(
        self, channels: List[int], tag: str, triggers: bool
    ) -> StatusReply:
        """
        Start raw recording with the selected channels
        :type channels: List[int]
        :type tag: str
          filename tag
        :type triggers: bool
          Save triggers or not
        """
        stub = IntanServiceStub(self.channel)
        saveinfo = SaveInfo(channels=channels, tag=tag, triggers=triggers)

        return await stub.startrecording(saveinfo)

    @classmethod
    async def start_raw_recording(cls, req: StartRawRecordingRequest) -> str:
        controller = cls()
        try:
            resp: StatusReply = await controller._start_raw_recording(
                req.channels, req.tag, req.triggers
            )
            if resp.status:
                return "Raw recording with the selected channels started successfully"
            else:
                return "Error when starting raw recording"
        finally:
            await controller._close()

    async def _stop_raw_recording(self) -> StatusReply:
        """
        Stop raw recording
        """
        stub = IntanServiceStub(self.channel)
        return await stub.stoprecording(Empty())

    @classmethod
    async def stop_raw_recording(cls) -> str:
        controller = cls()
        try:
            resp: StatusReply = await controller._stop_raw_recording()
            if resp.status:
                return "Raw recording stopped successfully"
            else:
                return "Error when stopping raw recording"
        finally:
            await controller._close()


async def var_threshold(req: VarThresholdRequest) -> str:
    validator = VarThresholdRequest(enable=req)
    return await IntanController.var_threshold(validator)


# async def impedance() -> str:
#     return await IntanController.impedance()


# async def set_count(req: CountListenerRequest) -> str:
#     validator = CountListenerRequest(triggers=req)
#     return await IntanController.set_count(validator)


# async def read_count() -> ReadCountResponse:
#     return await IntanController.read_count()


# async def set_tag_trigger(req: SetTagTriggerRequest) -> str:
#     validator = SetTagTriggerRequest(tag=req)
#     return await IntanController.set_tag_trigger(validator)


# async def send_stimparam(req: StimParamRequest) -> None:
#     validator = StimParamRequest(params=req)
#     return await IntanController.send_stimparam(validator)


# async def start_raw_recording(req: StartRawRecordingRequest) -> str:
#     validator = StartRawRecordingRequest(channels=req)
#     return await IntanController.start_raw_recording(validator)


# async def stop_raw_recording() -> str:
#     return await IntanController.stop_raw_recording()
