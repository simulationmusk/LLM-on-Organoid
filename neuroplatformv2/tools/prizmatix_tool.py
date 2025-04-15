from typing import Optional

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.prizmatix import PrizmatixController


class PrizmatixStarterTool(BaseTool):
    name = "start"
    description = "Start the Prizmatix UV led device"
    args_schema = BaseModel
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Start the Prizmatix UV led device
        """
        try:
            prizmatix_controller = PrizmatixController()
            return await prizmatix_controller.start()
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class PrizmatixStopperTool(BaseTool):
    name = "stop"
    description = "Stops the Prizmatix UV led device"
    args_schema = BaseModel
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Stops the Prizmatix UV led device
        """
        try:
            prizmatix_controller = PrizmatixController()
            return await prizmatix_controller.stop()
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
