from typing import Union

import requests

from ..utils.constants import PUMP_1_IP, PUMP_2_IP, PUMP_3_IP, PUMP_PORT
from ..utils.enumerations import PeristalticDirection, PumpId
from ..utils.schemas import (
    PeristalticRequest,
    PeristalticRpmRequest,
    PeristalticState,
)


class PeristalticController:
    """Control the peristaltic pump."""

    def __init__(self, id_pump: PumpId):
        """:param id_pump: id pump [1,2,3]"""
        self.id_pump = id_pump

    def _url(self, str: str):
        """Get url for the pump."""
        if self.id_pump == 1:
            url = f"http://{PUMP_1_IP}:{PUMP_PORT}/{str}/1"
        elif self.id_pump == 2:
            url = f"http://{PUMP_2_IP}:{PUMP_PORT}/{str}/2"
        elif self.id_pump == 3:
            url = f"http://{PUMP_3_IP}:{PUMP_PORT}/{str}/3"
        else:
            raise ValueError("id pump not [1,2,3]")

        return url

    def _start(self):
        """Start the pump"""
        url = self._url("start")
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False

    @classmethod
    def start(cls, req: PeristalticRequest) -> bool:
        controller = cls(req.pump_id)
        return controller._start()

    def _stop(self):
        """Stop the pump"""
        url = self._url("stop")
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False

    @classmethod
    def stop(cls, req: PeristalticRequest) -> bool:
        controller = cls(req.pump_id)
        return controller._stop()

    def _rpm(self, speed: float, direction: PeristalticDirection):
        """Set RPM speed and direction
        :type speed: float
        :type direction: PeristalticDirection
        Returns:
            PeristalticState: An instance of PeristalticState
        """
        url = self._url("set")
        r = requests.post(url, json={"rpm": speed, "direction": direction.value})
        if r.status_code == 200:
            return True
        else:
            return False

    @classmethod
    def rpm(cls, req: PeristalticRpmRequest) -> bool:
        controller = cls(req.pump_id)
        return controller._rpm(req.speed, req.direction)

    def _info(self) -> Union["PeristalticState", None]:
        """State of the pump"""
        url = self._url("info")
        r = requests.get(url)
        if r.status_code == 200:
            return PeristalticState.from_dict(r.json())
        else:
            return None

    @classmethod
    def info(cls, req: PeristalticRequest) -> Union["PeristalticState", None]:
        controller = cls(req.pump_id)
        return controller._info()


def start_peristaltic(req: PeristalticRequest) -> bool:
    validator = PeristalticRequest(pump_id=req.pump_id)
    return PeristalticController.start(validator)


def stop_peristaltic(req: PeristalticRequest) -> bool:
    validator = PeristalticRequest(pump_id=req.pump_id)
    return PeristalticController.stop(validator)


def rpm(req: PeristalticRpmRequest) -> bool:
    validator = PeristalticRpmRequest(
        speed=req.speed, direction=req.direction, pump_id=req.pump_id
    )
    return PeristalticController.rpm(validator)


def info(req: PeristalticRequest) -> "PeristalticState":
    validator = PeristalticRequest(pump_id=req.pump_id)
    return PeristalticController.info(validator)
