"""Meter classes."""

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)

from .energyradar import EnergyRadar
from .sensor import Sensor

_LOGGER = logging.getLogger(__name__)


class Meter:
    """Data and methods for interacting with an EnergyRadar meter."""

    def __init__(self, id, session, vendor=EnergyRadar):
        """Initialize meter."""
        self.id = id
        self._session = session
        self._vendor = vendor
        self.sensors = []

    def get_sensors(self) -> list[Sensor]:
        """Get sensors of this meter."""
        return self.sensors


class EnergyMeter(Meter):
    """Data and methods for interacting with an EnergyRadar meter."""

    def __init__(self, id, session, vendor=EnergyRadar):
        """Initialize meter."""
        self.id = id
        self._session = session
        self._vendor = vendor
        super().__init__(id, session=session, vendor=vendor)

        self.sensors.append(
            Sensor(
                self.id,
                "1.8.0",
                self._session,
                "Total Import",
                SensorDeviceClass.ENERGY,
                UnitOfEnergy.KILO_WATT_HOUR,
                SensorStateClass.TOTAL,
            )
        )
        self.sensors.append(
            Sensor(
                self.id,
                "1.8.0",
                self._session,
                "Import Cost",
                SensorDeviceClass.MONETARY,
                "EUR",
                SensorStateClass.TOTAL,
                field="cost",
            )
        )

        self.sensors.append(
            Sensor(
                self.id,
                "2.8.0",
                self._session,
                "Total Export",
                SensorDeviceClass.ENERGY,
                UnitOfEnergy.KILO_WATT_HOUR,
                SensorStateClass.TOTAL,
            )
        )
        self.sensors.append(
            Sensor(
                self.id,
                "2.8.0",
                self._session,
                "Export Cost",
                SensorDeviceClass.MONETARY,
                "EUR",
                SensorStateClass.TOTAL,
                field="cost",
            )
        )

        self.sensors.append(
            Sensor(
                self.id,
                "1.7.0",
                self._session,
                "Current Import",
                SensorDeviceClass.POWER,
                UnitOfPower.KILO_WATT,
                SensorStateClass.MEASUREMENT,
            )
        )
        self.sensors.append(
            Sensor(
                self.id,
                "2.7.0",
                self._session,
                "Current Export",
                SensorDeviceClass.POWER,
                UnitOfPower.KILO_WATT,
                SensorStateClass.MEASUREMENT,
            )
        )


class WaterMeter(Meter):
    """Data and methods for interacting with an EnergyRadar meter."""

    def __init__(self, id, session, vendor=EnergyRadar):
        """Initialize meter."""
        self.id = id
        self._session = session
        self._vendor = vendor
        super().__init__(id, session=session, vendor=vendor)

        self.sensors.append(
            Sensor(
                self.id,
                "1.0.0",
                self._session,
                "Total Import",
                SensorDeviceClass.WATER,
                UnitOfVolume.CUBIC_METERS,
                SensorStateClass.TOTAL,
            )
        )
        self.sensors.append(
            Sensor(
                self.id,
                "1.0.0",
                self._session,
                "Import Cost",
                SensorDeviceClass.MONETARY,
                "EUR",
                SensorStateClass.TOTAL,
                field="cost",
            )
        )

        self.sensors.append(
            Sensor(
                self.id,
                "2.0.0",
                self._session,
                "Flow Rate",
                SensorDeviceClass.VOLUME_FLOW_RATE,
                UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
                SensorStateClass.MEASUREMENT,
            )
        )


class GasMeter(Meter):
    """Data and methods for interacting with an EnergyRadar meter."""

    def __init__(self, id, session, vendor=EnergyRadar):
        """Initialize meter."""
        self.id = id
        self._session = session
        self._vendor = vendor
        super().__init__(id, session=session, vendor=vendor)

        self.sensors.append(
            Sensor(
                self.id,
                "3.0.0",
                self._session,
                "Total Import",
                SensorDeviceClass.GAS,
                UnitOfVolume.CUBIC_METERS,
                SensorStateClass.TOTAL,
            )
        )
        self.sensors.append(
            Sensor(
                self.id,
                "33.2.0",
                self._session,
                "Import Cost",
                SensorDeviceClass.MONETARY,
                "EUR",
                SensorStateClass.TOTAL,
                field="cost",
            )
        )
