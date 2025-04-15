from bson.objectid import ObjectId
from pymongo import MongoClient

from ..utils.constants import (
    MONGO_DB_IP,
    MONGO_DB_PASSWORD,
    MONGO_DB_PORT,
    MONGO_DB_USER,
)
from ..utils.enumerations import StimPolarity, StimShape
from ..utils.exceptions import (
    ExperimentControllerDataError,
    ExperimentControllerDBConnectionError,
    ExperimentControllerDBQueryError,
    ExperimentStartError,
    ExperimentStopError,
)
from ..utils.schemas import (
    ExperimentRequest,
    ExperimentStimParamRequest,
    StimParam,
)


class ExperimentController:
    """
    Experiment class for managing experimental procedures.

    Attributes:
        token (str): The unique token identifying the experiment.
        electrodes (list): List of electrodes.
        exp_name (str): The name of the experiment.
    """

    def __init__(self, token):
        """
        Initialize the ExperimentController instance.

        Args:
            token (str): The unique token identifying the experiment.

        Raises:
            Exception: If failed connecting to db
            Exception: If no experiment is found with the provided token.
            Exception: If the experiment cannot be run.
        """
        # Connect to MongoDB
        try:
            self._client = MongoClient(
                f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_IP}:{MONGO_DB_PORT}/"
            )
            self._db = self._client["neuroplatform"]
        except ExperimentControllerDBConnectionError:
            raise ExperimentControllerDBConnectionError(
                "Experiment controller failed connecting to the mongodb"
            )

        try:
            # Fetch the experiment document with the given token from the 'experiments' collection
            self._collection = self._db["experiments"]
            self.experiment = self._collection.find_one({"token": token})
            self.token = token
        except ExperimentControllerDBQueryError:
            raise ExperimentControllerDBQueryError(
                "Experiment controller failed querying db"
            )

        # Check if experiment document was found
        if self.experiment is None:
            raise ExperimentControllerDataError(
                f"No experiment found with token {token}"
            )

        # Check if can_run is False
        if not self.experiment.get("can_run", False):
            raise ExperimentControllerDataError("Error: Experiment cannot be run.")

        # Make electrodes and exp_name available in the object
        self.electrodes = self.experiment["electrodes"]
        self.exp_name = self.experiment["exp_name"]

    async def _start(self):
        """
        Start the experiment.

        Returns:
            bool: True if the experiment was started successfully, False otherwise.
        """
        # Connect to the 'intan' collection
        intan_collection = self._db["intan"]

        # Fetch the current status of the document
        current_status = intan_collection.find_one(
            {"_id": ObjectId("651c6fa7f916078db0ebcecd")}
        )

        # Check if exp_running is True
        if current_status.get("exp_running", False):
            print("Experiment is already running!")
            return False

        # Check if maintenance is True
        if current_status.get("maintenance", False):
            print("System is currently under maintenance!")
            return False

        # Re-fetch the experiment document to check if can_run is still True
        refreshed_experiment = self._collection.find_one({"token": self.token})
        if not refreshed_experiment.get("can_run", False):
            print("Error: Experiment cannot be run.")
            return False

        # Update the document in the 'intan' collection to set 'exp_running' to True
        intan_collection.update_one(
            {"_id": ObjectId("651c6fa7f916078db0ebcecd")},
            {"$set": {"exp_running": True, "token": self.token}},
        )
        return True

    @classmethod
    async def start(cls, req: ExperimentRequest) -> bool:
        try:
            controller = cls(req.token)
            return await controller._start()
        except ExperimentStartError:
            return False

    async def _stop(self):
        """
        Stop the experiment.

        Returns:
            bool: True if the experiment was stopped successfully, False otherwise.
        """
        # Connect to the 'intan' collection
        intan_collection = self._db["intan"]

        # Fetch the current status of the document
        current_status = intan_collection.find_one(
            {"_id": ObjectId("651c6fa7f916078db0ebcecd")}
        )

        # Check if the tokens match
        if current_status.get("token") != self.token:
            print("Error: Token mismatch!")
            return False

        # Update the document in the 'intan' collection to set 'exp_running' to False
        intan_collection.update_one(
            {"_id": ObjectId("651c6fa7f916078db0ebcecd")},
            {"$set": {"exp_running": False}},
        )
        return True

    @classmethod
    async def stop(cls, req: ExperimentRequest) -> bool:
        try:
            controller = cls(req.token)
            return await controller._stop()
        except ExperimentStopError:
            return False

    async def _best_stim_param(self, index_electrode: int):
        """
        Get the best stimparam for an electrode

        Args:
            index_electrode (int): Index electrode.
        Returns:
            StimParam: Best stimulation Parameter
            datetime: The last update time of the best stim parameter
        Raises:
            Exception: If index electrode out of range
        """
        try:
            col = self._db["best_stim_param"]
            best_param = col.find_one({"index": index_electrode}, {"_id": 0})
        except ExperimentControllerDBQueryError:
            return None

        sp = StimParam()
        sp.index = best_param["index"]
        sp.polarity = StimPolarity(best_param["polarity"])
        sp.phase_duration1 = best_param["phase_duration1"]
        sp.phase_amplitude1 = best_param["amplitude1"]
        sp.phase_duration2 = best_param["phase_duration2"]
        sp.phase_amplitude2 = best_param["amplitude2"]
        sp.stim_shape = StimShape(best_param["shape"])
        sp.interphase_delay = best_param["interphase_delay"]
        return sp, best_param["updated"]

    @classmethod
    async def best_stim_param(cls, req: ExperimentStimParamRequest) -> StimParam | None:
        try:
            controller = cls(req.token)
            return await controller._best_stim_param(req.index_electrode)
        except ExperimentControllerDBQueryError:
            return None


async def start_experiment(req: ExperimentRequest) -> bool:
    validator = ExperimentRequest(token=req.token)
    return await ExperimentController.start(validator)


async def stop_experiment(req: ExperimentRequest) -> bool:
    validator = ExperimentRequest(token=req.token)
    return await ExperimentController.stop(validator)


async def best_stim_param(req: ExperimentStimParamRequest) -> StimParam | None:
    validator = ExperimentStimParamRequest(
        token=req.token, index_electrode=req.index_electrode
    )
    return await ExperimentController.best_stim_param(validator)
