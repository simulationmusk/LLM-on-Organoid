from typing import Optional, Type, Union

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
)
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.peristaltic import PeristalticController
from ..utils.schemas import (
    PeristalticRequest,
    PeristalticRpmRequest,
    PeristalticState,
)


class PeristalticStarterTool(BaseTool):
    name = "start"
    description = "Start the peristaltic pump"
    args_schema = PeristalticRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = PeristalticRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Use the tool to Start the peristaltic pump
        """
        try:
            peristaltic_controller = PeristalticController(req.pump_id)
            return await peristaltic_controller.start(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class PeristalticStopperTool(BaseTool):
    name = "stop"
    description = "Stop the peristaltic pump"
    args_schema = PeristalticRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = PeristalticRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Use the tool to Stop the peristaltic pump.
        """
        try:
            peristaltic_controller = PeristalticController(req.pump_id)
            return await peristaltic_controller.stop(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class PeristalticRPMTool(BaseTool):
    name = "rpm"
    description = "Set RPM speed and direction of peristaltic pump"
    args_schema = PeristalticRpmRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: PeristalticRpmRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Use the tool to set RPM speed and direction of peristaltic pump.
        """
        try:
            peristaltic_controller = PeristalticController(req.pump_id)
            return await peristaltic_controller.rpm(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class PeristalticInfoTool(BaseTool):
    name = "info"
    description = "Get state of the peristaltic pump"
    args_schema = PeristalticRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = PeristalticRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Union[PeristalticState, None]:
        """
        Use the tool to get state of the peristaltic pump.
        """
        try:
            peristaltic_controller = PeristalticController(req.pump_id)
            return await peristaltic_controller.info(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
