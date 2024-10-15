"""Sensor class."""

from .schemas import METER_CALCULATED


class Sensor:
    """A single sensor of a meter."""

    def __init__(
        self,
        meter_id,
        code,
        session,
        name,
        device_class,
        unit,
        state_class,
        manufacturer="EnergyRadar",
        field="value",
        display_unit=None,
    ):
        """Initialize sensor."""
        self.meter_id = meter_id
        self.code = code
        self.name = name
        self._session = session
        self.device_class = device_class
        self.unit = unit
        self.display_unit = display_unit
        self.state_class = state_class
        self.manufacturer = manufacturer
        self.field = field

    @property
    def get_value(self) -> float | int:
        """Get sensor value."""
        resp = self._session.get(
            f"/v1/meters/{self.meter_id}/calculations",
            params={"obisCodesFilter": self.code},
        )
        meter_calculated = METER_CALCULATED(resp.json())
        return meter_calculated["data"][0]["obis"][self.code][self.field]
