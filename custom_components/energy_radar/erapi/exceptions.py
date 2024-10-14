"""Exceptions for EnergyRadar API."""


class EnergyRadarException(Exception):
    """General energyradar exception."""


class EnergyRadarLoginException(EnergyRadarException):
    """To indicate there is a login issue."""


class EnergyRadarMeterException(EnergyRadarException):
    """To be thrown anytime there is a meter error."""


class EnergyRadarUnsupportedDevice(EnergyRadarMeterException):
    """To be thrown only for unsupported devices."""
