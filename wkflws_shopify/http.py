from dataclasses import dataclass
import json
from logging import Logger
import time
from typing import Any, Optional
import urllib.error
import urllib.request

from .encoders import ShopifyJSONEncoder


class HttpError(Exception):
    """Describe an unrecoverable HTTP Error."""

    def __init__(self, msg, status_code, body):
        self.status_code = status_code
        self.body = body
        super().__init__(msg)


@dataclass
class HttpResponse:
    """Describe an HTTP response."""

    status_code: int
    headers: dict[str, str]
    body: bytes

    def json(self):
        """Attempt to deserialize and return a JSON response body."""
        return json.loads(self.body)


def make_http_request(
    logger: Logger,
    *,
    myshopify_domain: str,
    api_path: str,
    api_token: str,
    json_data: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, Any]] = None,
    method: Optional[str] = None,
    num_retries: int = 5,
    api_version: str = "2022-04",
) -> HttpResponse:
    """Make an HTTP request.

    Args:
        myshopify_domain: The store's full myshopify domain (shop.myshopif.com)
        api_path: The path of the api to use.
        api_token: The API token for the shopify shop.
        json_data: A JSON serializable payload to send to the API.
        headers: Headers to include in the request.
        method: The HTTP method (e.g. GET, POST, etc)
        num_retries: Number of retries (exponentially backed off) when receiving a
            server error before failing.


    Raises
        HttpError: The error response from the HTTP request.

    Returns:
        The response from the HTTP request.
    """
    url = f"https://{myshopify_domain}/admin/api/{api_version}{api_path}"
    if headers is None:
        headers = {}

    headers.update(
        {
            "X-Shopify-Access-Token": api_token,
        }
    )
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json; charset=utf-8"

    payload = (
        json.dumps(json_data, cls=ShopifyJSONEncoder).encode("utf-8")
        if json_data
        else None
    )
    request = urllib.request.Request(
        url,
        data=payload,
        headers=headers or {},
        method=method,
    )

    retry_count = 0
    while True:
        logger.info(f"Making HTTP request to {url}...")
        try:
            _r = urllib.request.urlopen(request)
            response = HttpResponse(
                status_code=_r.status,
                headers={k: v for k, v in _r.headers.items()},
                body=_r.read(),
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")

            if e.status is None:
                raise HttpError(
                    f"Unknown HTTP Error {e}",
                    status_code=e.status,
                    body=body,
                ) from None

            if e.status == 429 or (e.status >= 500 and e.status < 600):
                # Server error. Wait and retry
                retry_count += 1
                if retry_count > num_retries:
                    # Retries exceeded. Log message so we know about it
                    raise HttpError(
                        "Retries Exceed",
                        status_code=e.status,
                        body=body,
                    ) from None
                wait_for = 2**retry_count
                logger.debug(
                    f"Request failed. Waiting {wait_for}s before retrying. "
                    f"({retry_count} of {num_retries})"
                )
                time.sleep(wait_for)
                continue
            elif e.status >= 400 and e.status < 500:
                # Client error. Log the message so it can be fixed.
                raise HttpError(
                    f"HTTP Error {e.status}",
                    status_code=e.status,
                    body=body,
                ) from None
            else:
                # Unknown error. Log so it can be looked into.
                raise HttpError(
                    f"Unknown HTTP Error {e.status}",
                    status_code=e.status,
                    body=body,
                ) from None

        if response.status_code >= 200 and response.status_code < 300:
            # Successful request
            return response
        elif response.status_code >= 300 and response.status_code < 400:
            # Location moved:
            return make_http_request(
                logger,
                url=response.headers["Location"],
                api_token=api_token,
                json_data=json_data,
                headers=headers,
                method=method,
            )
        else:
            return response
