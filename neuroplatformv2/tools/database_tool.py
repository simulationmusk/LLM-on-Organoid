from typing import Optional, Type

import pandas as pd
from langchain.tools import BaseTool
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.database import DatabaseController
from ..utils.schemas import (
    RawSpikeQuery,
    SpikeCountQuery,
    SpikeEventQuery,
    TriggersQuery,
)


class ExperimentGetSpikeEventTool(BaseTool):
    name = "get_spike_event"
    description = "Get spike event from db."
    args_schema: Type[BaseModel] = SpikeEventQuery
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = SpikeEventQuery,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Use the tool to get spike event from db.
        """
        try:
            db_controller = DatabaseController()
            return await db_controller.get_spike_event(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class ExperimentGetRawSpikeTool(BaseTool):
    name = "get_raw_spike"
    description = "Get raw spike from db."
    args_schema: Type[BaseModel] = RawSpikeQuery
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = RawSpikeQuery,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> pd.DataFrame:
        """
        Use the tool to get raw spike from db.
        """
        try:
            db_controller = DatabaseController()
            return await db_controller.get_raw_spike(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class ExperimentGetSpikeCountTool(BaseTool):
    name = "get_spike_count"
    description = "Get spike count from db."
    args_schema: Type[BaseModel] = SpikeCountQuery
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = SpikeCountQuery,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> pd.DataFrame:
        """
        Use the tool to Get spike count from db.
        """
        try:
            db_controller = DatabaseController()
            return await db_controller.get_spike_count(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class ExperimentGetAllTriggersTool(BaseTool):
    name = "get_all_triggers"
    description = "Get all triggers from db."
    args_schema: Type[BaseModel] = TriggersQuery
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = TriggersQuery,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> pd.DataFrame:
        """
        Use the tool to get all triggers from db.
        """
        try:
            db_controller = DatabaseController()
            return await db_controller.get_all_triggers(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
