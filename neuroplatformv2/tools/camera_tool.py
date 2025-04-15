from typing import Optional, Type

import numpy as np
import pandas as pd
from langchain.tools import BaseTool
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain_core.tools import ToolException
from pydantic import BaseModel

from ..core.camera import CameraController
from ..utils.schemas import (
    CameraCaptureRequest,
    CameraFromRequest,
    CameraListImagesRequest,
)


class CameraImageFromTool(BaseTool):
    name = "image_from"
    description = "Get image with the ID."
    args_schema: Type[BaseModel] = CameraFromRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CameraFromRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Optional[np.ndarray]:
        """
        Use the tool to get image with the ID.
        """
        try:
            camera_controller = CameraController(req.mea)
            return await camera_controller.image_from(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class CameraThumbnailFromTool(BaseTool):
    name = "thumbnail_from"
    description = "Get thumbnail with the ID."
    args_schema: Type[BaseModel] = CameraFromRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CameraFromRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Optional[np.ndarray]:
        """
        Use the tool to get thumbnail with the ID.
        """
        try:
            camera_controller = CameraController(req.mea)
            return await camera_controller.thumbnail_from(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class CameraListImagesTool(BaseTool):
    name = "list_images"
    description = "List images taken during the interval."
    args_schema: Type[BaseModel] = CameraListImagesRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CameraListImagesRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> pd.DataFrame:
        """
        Use the tool to list images taken during the interval.
        """
        try:
            camera_controller = CameraController(req.mea)
            return await camera_controller.list_images(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class CameraLastCaptureTool(BaseTool):
    name = "last_capture"
    description = "Get last capture of a MEA."
    args_schema: Type[BaseModel] = CameraCaptureRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CameraCaptureRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> pd.DataFrame:
        """
        Use the tool to get last capture of a MEA
        """
        try:
            camera_controller = CameraController(req.mea)
            return await camera_controller.last_capture(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))


class CameraCaptureTool(BaseTool):
    name = "capture"
    description = "Capture MEA."
    args_schema: Type[BaseModel] = CameraCaptureRequest
    handle_tool_error = True
    handle_validation_error = True

    def _run(self):
        return ""  # ! We need to implement this method to run the tool otherwise we're getting an error

    async def _arun(
        self,
        req: Type[BaseModel] = CameraCaptureRequest,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> np.ndarray:
        """
        Use the tool to capture MEA.
        """
        try:
            camera_controller = CameraController(req.mea)
            return await camera_controller.capture(req)
        except Exception as e:
            # Wrap any exception into a ToolException
            raise ToolException(str(e))
