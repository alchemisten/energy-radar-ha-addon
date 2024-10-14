"""Energyradar Authenficiation."""

from collections.abc import Callable
import logging
from urllib.parse import urljoin

from oauthlib.oauth2 import TokenExpiredError
import requests
from requests_oauthlib import OAuth2Session

from .energyradar import EnergyRadar, Vendor
from .exceptions import EnergyRadarException

_LOGGER = logging.getLogger(__name__)


class Session:
    """Base session."""

    def __init__(self, vendor: Vendor) -> None:
        """Initialize the session."""
        self.vendor = vendor
        self.endpoint = vendor.endpoint

    def get(self, path, **kwargs):
        """Send a GET request to the specified path."""
        raise NotImplementedError

    def urljoin(self, path):
        """Join URLs."""
        return urljoin(self.endpoint, path)


class OAuthSession(Session):
    """OAuth Session."""

    def __init__(
        self,
        token: dict[str, str] | None = None,
        client_id: str | None = None,
        redirect_uri: str | None = None,
        token_updater: Callable[[str], None] | None = None,
        vendor: Vendor = EnergyRadar(),
    ) -> None:
        """Initialize OAuth Session."""
        super().__init__(vendor=vendor)

        self._client_id = client_id
        self._redirect_uri = redirect_uri
        self._token_updater = token_updater
        self._vendor = vendor

        extra = {"client_id": self._client_id}

        self._oauth = OAuth2Session(
            auto_refresh_kwargs=extra,
            client_id=client_id,
            token=token,
            redirect_uri=redirect_uri,
            token_updater=token_updater,
            scope=vendor.scope,
        )

    def refresh_tokens(self) -> dict:
        """Refresh and return new tokens."""
        token = self._oauth.refresh_token(f"{self._vendor.token_endpoint}")

        if self._token_updater is not None:
            self._token_updater(token)

        return token

    def get_authorization_url(self) -> str:
        """Get an authorization url via oauth2."""

        authorization_url, state = self._oauth.authorization_url(
            self.vendor.auth_endpoint
        )
        return authorization_url

    def fetch_token(self, authorization_response: str) -> dict[str, str]:
        """Fetch an access token via oauth2."""
        return self._oauth.fetch_token(
            self.vendor.token_endpoint,
            authorization_response=authorization_response,
        )

    def get(self, path: str, **kwargs) -> requests.Response:
        """Make a get request.

        We don't use the built-in token refresh mechanism of OAuth2 session because
        we want to allow overriding the token refresh logic.
        """
        url = self.urljoin(path)
        try:
            response = self._get(url, **kwargs)
            response.raise_for_status()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
        ) as ex:
            raise EnergyRadarException(
                "Unable to connect to the energyradar server."
            ) from ex
        return response

    def _get(self, path: str, **kwargs) -> requests.Response:
        """Get request without error handling.

        Refreshes the token if necessary.
        """
        try:
            return self._oauth.get(path, **kwargs)
        except TokenExpiredError:
            self._oauth.token = self.refresh_tokens()

            return self._oauth.get(path, **kwargs)
