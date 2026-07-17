from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class SourceFetchError(RuntimeError):
    pass


@dataclass(frozen=True)
class FetchedSource:
    requested_url: str
    final_url: str
    status_code: int
    content_type: str
    encoding: str
    body: str
    byte_count: int


Transport = Callable[[str, float, int], FetchedSource]


class UrlSourceFetcher:
    """Fetch public HTTP(S) article pages with conservative safety limits."""

    def __init__(self, transport: Transport | None = None, *, timeout: float = 10.0, max_bytes: int = 2_000_000):
        self.transport = transport or self._default_transport
        self.timeout = timeout
        self.max_bytes = max_bytes

    def fetch(self, url: str) -> FetchedSource:
        self._validate_public_url(url)
        try:
            fetched = self.transport(url, self.timeout, self.max_bytes)
        except SourceFetchError:
            raise
        except Exception as exc:
            raise SourceFetchError(f"source fetch failed: {exc}") from exc
        self._validate_public_url(fetched.final_url)
        if fetched.status_code < 200 or fetched.status_code >= 300:
            raise SourceFetchError(f"unexpected HTTP status: {fetched.status_code}")
        content_type = fetched.content_type.lower()
        if not (content_type.startswith("text/html") or content_type.startswith("text/plain")):
            raise SourceFetchError(f"unsupported content type: {fetched.content_type}")
        if not fetched.body.strip():
            raise SourceFetchError("fetched source is empty")
        return fetched

    @staticmethod
    def _validate_public_url(url: str) -> None:
        parts = urlsplit((url or "").strip())
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            raise SourceFetchError("only absolute http/https URLs are allowed")
        host = parts.hostname.rstrip(".").lower()
        if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
            raise SourceFetchError("local network URLs are not allowed")
        try:
            addresses = {item[4][0] for item in socket.getaddrinfo(host, parts.port or (443 if parts.scheme == "https" else 80))}
        except socket.gaierror as exc:
            raise SourceFetchError(f"host resolution failed: {host}") from exc
        for address in addresses:
            ip = ipaddress.ip_address(address)
            if not ip.is_global:
                raise SourceFetchError("private, loopback, link-local, or reserved network addresses are not allowed")

    @staticmethod
    def _default_transport(url: str, timeout: float, max_bytes: int) -> FetchedSource:
        request = Request(
            url,
            headers={
                "User-Agent": "SIMS-Writer/1.2 (+article-source-fetch)",
                "Accept": "text/html,text/plain;q=0.9,*/*;q=0.1",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise SourceFetchError(f"source exceeds {max_bytes} bytes")
                content_type = response.headers.get_content_type() or "application/octet-stream"
                encoding = response.headers.get_content_charset() or "utf-8"
                try:
                    body = raw.decode(encoding)
                except (LookupError, UnicodeDecodeError):
                    encoding = "utf-8"
                    body = raw.decode("utf-8", errors="replace")
                return FetchedSource(
                    requested_url=url,
                    final_url=response.geturl(),
                    status_code=int(getattr(response, "status", 200)),
                    content_type=content_type,
                    encoding=encoding,
                    body=body,
                    byte_count=len(raw),
                )
        except HTTPError as exc:
            raise SourceFetchError(f"HTTP error: {exc.code}") from exc
        except URLError as exc:
            raise SourceFetchError(f"network error: {exc.reason}") from exc
