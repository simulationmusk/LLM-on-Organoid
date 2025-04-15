from datetime import datetime
from typing import Optional, Union

import cv2
import numpy as np
import pandas as pd
import requests
from dateutil import parser

from ..utils.constants import CAMERA_IP, CAMERA_PORT
from ..utils.enumerations import MEA
from ..utils.exceptions import CameraReadingError
from ..utils.schemas import (
    CameraCaptureRequest,
    CameraFromRequest,
    CameraListImagesRequest,
)

# MARK: Main business logic


class CameraController:
    """
    CameraController class to access and take picture of MEA
    """

    def __init__(self, mea: MEA):
        self._mea = mea

    def _image_from(self, img_id: str) -> Optional[np.ndarray]:
        """
        Get image with the ID
        :type img_id: str

        :return:
            np.array: image in RGB
        """
        r = requests.get(f"http://{CAMERA_IP}:{CAMERA_PORT}/image/{img_id}")
        if r.status_code == 200:
            jpg_original = r.content
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        else:
            raise CameraReadingError(
                f"Status code: {r.status_code}, Image not available"
            )

    @classmethod
    def image_from(cls, req: CameraFromRequest) -> Optional[np.ndarray]:
        """
        Get image with the ID
        :type req: CameraFromRequest

        :return:
            np.array: image in RGB
        """
        r = requests.get(f"http://{CAMERA_IP}:{CAMERA_PORT}/image/{req.img_id}")
        if r.status_code == 200:
            jpg_original = r.content
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        else:
            raise CameraReadingError(
                f"Status code: {r.status_code}, Image not available"
            )

    @classmethod
    def thumbnail_from(cls, req: CameraFromRequest) -> Optional[np.ndarray]:
        """
        Get thumbnail with the ID.
        :type req: CameraFromRequest

        :return:
            np.array: image in RGB
        """
        r = requests.get(f"http://{CAMERA_IP}:{CAMERA_PORT}/thumb/{req.img_id}")
        if r.status_code == 200:
            jpg_original = r.content
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        else:
            raise CameraReadingError(
                f"Status code: {r.status_code}, Image not available"
            )

    async def _list_images(
        self, start_date: Union[str, datetime], end_date: Union[str, datetime]
    ):
        """
        List images taken during the interval
        :type start_date: datetime
        :type end_date: datetime

        :return pd.DataFrame
        """
        # Ensuring the provided dates are in datetime format.
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        # Constructing the payload
        payload = {"start": start_date.isoformat(), "end": end_date.isoformat()}

        # Making the POST request
        response = requests.post(
            f"http://{CAMERA_IP}:{CAMERA_PORT}/listimage", json=payload
        )

        # Handle possible HTTP errors
        response.raise_for_status()

        # Convert response JSON to list of ImageData
        data = response.json()

        index_mea = self._mea.value
        if self._mea == MEA.One:
            index_mea = None

        images = []
        for item in data:
            index = item.get("index")
            if index == index_mea:
                images.append({"id": item["id"], "date": parser.parse(item["date"])})

        return pd.DataFrame(data=images)

    # MARK: Public methods/class methods

    @classmethod
    async def list_images(cls, req: CameraListImagesRequest) -> pd.DataFrame:
        controller = cls(req.mea)
        return await controller._list_images(req.start_date, req.end_date)

    async def _last_capture(self):
        """
        Get last capture of a MEA

        :return pd.DataFrame
        """
        r = requests.get(f"http://{CAMERA_IP}:{CAMERA_PORT}/lastcapture")
        r.raise_for_status()
        data = r.json()
        index_img = data[self._mea.value]

        r = requests.get(
            f"http://{CAMERA_IP}:{CAMERA_PORT}/imageinfo/{index_img['_id']}"
        )
        r.raise_for_status()
        data = r.json()
        date = data["date"]

        return pd.DataFrame(data=[{"id": index_img["_id"], "date": parser.parse(date)}])

    @classmethod
    async def last_capture(cls, req: CameraCaptureRequest) -> pd.DataFrame:
        controller = cls(req.mea)
        return await controller._last_capture()

    async def _capture(self):
        """
        Capture MEA

        :return img: np.array
        """
        r = requests.get(f"http://172.30.1.221:5000/capture_cam/{self._mea.value}")
        r.raise_for_status()

        jpg_original = r.content
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    @classmethod
    async def capture(cls, req: CameraCaptureRequest) -> np.ndarray:
        controller = cls(req.mea)
        return await controller._capture()


# MARK: Functions for tools


def image_from(req: CameraFromRequest):
    validator = CameraFromRequest(img_id=req.img_id)
    return CameraController.image_from(validator)


def thumbnail_from(req: CameraFromRequest):
    validator = CameraFromRequest(img_id=req.img_id)
    return CameraController.thumbnail_from(validator)


async def list_images(req: CameraListImagesRequest) -> pd.DataFrame:
    validator = CameraListImagesRequest(
        mea=req.mea, start_date=req.start_date, end_data=req.end_date
    )
    return await CameraController.list_images(validator)


async def last_capture(req: CameraCaptureRequest) -> pd.DataFrame:
    validator = CameraCaptureRequest(mea=req.mea)
    return await CameraController.last_capture(validator)


async def capture(req: CameraCaptureRequest) -> np.ndarray:
    validator = CameraCaptureRequest(mea=req.mea)
    return await CameraController.capture(validator)
