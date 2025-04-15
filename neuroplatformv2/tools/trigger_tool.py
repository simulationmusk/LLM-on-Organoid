from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
)
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.trigger import TriggerController
from ..utils.schemas import TriggerPattern


class TriggerSenderTool(BaseTool):
    name = "trigger_sender"
    description = "Sends a trigger pattern to the neuro stimulation platform."
    args_schema: Type[BaseModel] = TriggerPattern
    handle_tool_error = True
    handle_validation_error = True

    def _run():
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        pattern: Type[BaseModel] = TriggerPattern,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to send a trigger pattern.
        """
        try:
            trigger_controller = await TriggerController()
            return await trigger_controller.trigger_sender(pattern)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
