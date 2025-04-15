class TriggerConnectionError(Exception):
    """Exception raised when there's an issue connecting to or communicating with the trigger device."""

    pass


class IntanConnectionError(Exception):
    """Exception raised when connecting to Intan software"""

    pass


class TriggerUVConnectionError(Exception):
    """Exception raised when connecting to Trigger UV"""

    pass


class TriggerUVSendError(Exception):
    """Exception when sending data from Trigger UV"""

    pass


class DatabaseConnectionError(Exception):
    """Exception when connecting to db"""

    pass


class DatabaseQueryError(Exception):
    """Exception when querying db"""

    pass


class ExperimentControllerDBConnectionError(Exception):
    """Exception class for connecting db from ExperimentController"""

    pass


class ExperimentControllerDBQueryError(Exception):
    """Exception class for errors when querying from data db by ExperimentController"""

    pass


class ExperimentControllerDataError(Exception):
    """Exception class related to data read from db in ExperimentController"""

    pass


class ExperimentStartError(Exception):
    """Exception related to staring an experiment"""

    pass


class ExperimentStopError(Exception):
    """Exception related to stopping an experiment"""

    pass


class CameraReadingError(Exception):
    """Exception class for reading camera"""

    pass
