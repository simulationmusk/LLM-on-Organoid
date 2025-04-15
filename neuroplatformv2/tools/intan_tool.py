from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
)
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.intan import IntanController
from ..utils.schemas import (
    CountListenerRequest,
    ReadCountResponse,
    SetTagTriggerRequest,
    StartRawRecordingRequest,
    StimParamRequest,
    VarThresholdRequest,
)


class IntanVarThresholdTool(BaseTool):
    name = "var_threshold"
    description = "Enable/disable auto variation threshold."
    args_schema: Type[BaseModel] = VarThresholdRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = VarThresholdRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to enable/disable auto variation threshold.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.var_threshold(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanImpedanceTool(BaseTool):
    name = "impedance"
    description = "Run impedance measurement"
    args_schema: Type[BaseModel] = BaseModel
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to run impedance measurement.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.impedance()
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanSetCountTool(BaseTool):
    name = "set_count"
    description = "Set count listener on selected triggers."
    args_schema: Type[BaseModel] = CountListenerRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CountListenerRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to set count listener on selected triggers.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.set_count(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanReadCountTool(BaseTool):
    name = "read_count"
    description = "Get the number of spike (of all electrodes) after triggers selected."
    args_schema: Type[BaseModel] = BaseModel
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> ReadCountResponse:
        """
        Use the tool to get the number of spike (of all electrodes) after triggers selected.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.read_count()
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanSetTagTriggerTool(BaseTool):
    name = "set_tag_trigger"
    description = (
        "Set tag to trigger. It will be store in the database with all triggers"
    )
    args_schema: Type[BaseModel] = SetTagTriggerRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = SetTagTriggerRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to set tag to trigger. It will be store in the database with all triggers.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.set_tag_trigger(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanSendStimParamTool(BaseTool):
    name = "send_stimparam"
    description = "Send a list of stim parameter to intan software."
    args_schema: Type[BaseModel] = StimParamRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = StimParamRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> None:
        """
        Use the tool to send a list of stim parameter to intan software.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.send_stimparam(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanStartRawRecordingTool(BaseTool):
    name = "start_raw_recording"
    description = "Start raw recording with the selected channels."
    args_schema: Type[BaseModel] = StartRawRecordingRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = StartRawRecordingRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to start raw recording with the selected channels.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.start_raw_recording(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class IntanStopRawRecordingTool(BaseTool):
    name = "stop_raw_recording"
    description = "Stop raw recording."
    args_schema: Type[BaseModel] = BaseModel
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to Stop raw recording.
        """
        try:
            intan_controller = IntanController()
            return await intan_controller.stop_raw_recording()
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
