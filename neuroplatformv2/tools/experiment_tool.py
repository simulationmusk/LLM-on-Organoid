from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.experiment import ExperimentController
from ..utils.schemas import (
    ExperimentRequest,
    ExperimentStimParamRequest,
    StimParam,
)


class ExperimentStarterTool(BaseTool):
    name = "start"
    description = "Start the experiment."
    args_schema: Type[BaseModel] = ExperimentRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = ExperimentRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Use the tool to start the experiment.
        """
        try:
            experiment_controller = ExperimentController(req.token)
            return await experiment_controller.start(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class ExperimentStopperTool(BaseTool):
    name = "stop"
    description = "Stop the experiment."
    args_schema: Type[BaseModel] = ExperimentRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = ExperimentRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> bool:
        """
        Use the tool to stop the experiment.
        """
        try:
            experiment_controller = ExperimentController(req.token)
            return await experiment_controller.stop(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class ExperimentBestStimParamTool(BaseTool):
    name = "best_stim_param"
    description = "Get the best stimparam for an electrode."
    args_schema: Type[BaseModel] = ExperimentStimParamRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = ExperimentStimParamRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> StimParam | None:
        """
        Use the tool to get the best stimparam for an electrode.
        """
        try:
            experiment_controller = ExperimentController(req.token)
            return await experiment_controller.best_stim_param(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
