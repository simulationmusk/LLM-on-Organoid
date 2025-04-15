from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.triggeruv import TriggerUVController
from ..utils.schemas import TriggerUVSendRequest


class TriggerUVSenderTool(BaseTool):
    name = "trigger_uv_send"
    description = "Control the trigger UV. Only 1 trigger to activate the UV. Power Control is manual (potentiometer)"
    args_schema: Type[BaseModel] = TriggerUVSendRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = TriggerUVSendRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Use the tool to send a trigger uv pattern to activate the UV for a period of t
        """
        try:
            trigger_controller = TriggerUVController()
            return await trigger_controller.trigger_uv_send(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
