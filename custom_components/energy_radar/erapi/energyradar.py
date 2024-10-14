"""EnergyRadar vendor classes."""

from dataclasses import dataclass


@dataclass(init=False, frozen=True)
class Vendor:
    """Basic vendor class."""

    name: str
    endpoint: str
    auth_endpoint: str
    token_endpoint: str
    scope: list[str]


class EnergyRadar(Vendor):
    """EnergyRadar vendor."""

    name = "energyradar"
    endpoint = "https://feature-historic-data.api.energyradar.net"
    auth_endpoint = "https://account-test.api.energyradar.net/realms/energy-radar/protocol/openid-connect/auth"
    token_endpoint = "https://account-test.api.energyradar.net/realms/energy-radar/protocol/openid-connect/token"
    scope = ["user_meters"]
