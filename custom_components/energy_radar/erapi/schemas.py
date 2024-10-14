"""Schemas for JSON parsing."""

from voluptuous import All, Any, Required, Schema

OBIS_SCHEMA = Schema(
    {
        Required("code"): str,
        Required("unit"): int,
        Required("scale"): int,
    }
)

# Define the schema for a Meter
METER_SCHEMA = Schema(
    {
        Required("meterId"): str,
        Required("obisMedium"): str,
        Required("availableObisValues"): [OBIS_SCHEMA],
        Required("relatedMeters"): [
            str
        ],  # Assuming it's a list of related meter IDs as strings
    }
)

# Define the schema for the entire data structure
METERS_SCHEMA = Schema(
    {Required("count"): int, Required("offset"): int, Required("data"): [METER_SCHEMA]}
)

METER_CALCULATED_DATA_POINT = Schema(
    {
        Required("time"): str,
        Required("obis"): Schema(
            {
                str: Schema(
                    {
                        "value": Any(float, int),
                        Any("agg", None): Schema(
                            {
                                "cumSum": Schema(
                                    {
                                        "lbp": Schema(
                                            {"v": Any(float, int), "c": Any(float, int)}
                                        ),
                                        "som": Schema(  # codespell:ignore som
                                            {"v": Any(float, int), "c": Any(float, int)}
                                        ),
                                        "sod": Schema(  # codespell:ignore sod
                                            {"v": Any(float, int), "c": Any(float, int)}
                                        ),
                                    }
                                )
                            }
                        ),
                        Any("cost", None): Any(float, int),
                        Any("delta", None): Schema(
                            {"v": Any(float, int), "c": Any(float, int)}
                        ),
                    }
                )
            }
        ),
    }
)

METER_CALCULATED = Schema(
    {
        Required("meterId"): str,
        Required("obisMedium"): str,
        Required("data"): All([METER_CALCULATED_DATA_POINT]),
    }
)
