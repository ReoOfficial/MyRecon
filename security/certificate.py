import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse


def _extract_common_name(
    certificate: dict,
) -> str | None:
    """
    Extract the Common Name (CN) from a certificate.
    """
    for subject_item in certificate.get("subject", ()):
        for key, value in subject_item:
            if key == "commonName":
                return value

    return None


def _extract_expiration_date(
    certificate: dict,
) -> str | None:
    """
    Extract and convert the certificate expiration date.
    """
    expiration = certificate.get("notAfter")

    if not expiration:
        return None

    timestamp = ssl.cert_time_to_seconds(expiration)

    expiration_date = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    )

    return expiration_date.isoformat()


def get_https_information(
    url: str,
    timeout: float = 5.0,
) -> dict:
    """
    Collect HTTPS and SSL/TLS certificate information.
    """
    parsed_url = urlparse(url)

    if parsed_url.scheme != "https":
        return {
            "enabled": False,
            "certificate_cn": None,
            "certificate_expiration": None,
        }

    hostname = parsed_url.hostname

    if hostname is None:
        return {
            "enabled": True,
            "certificate_cn": None,
            "certificate_expiration": None,
            "certificate_error": "Hostname unavailable.",
        }

    port = parsed_url.port or 443

    context = ssl.create_default_context()

    try:
        with socket.create_connection(
            (hostname, port),
            timeout=timeout,
        ) as connection:
            with context.wrap_socket(
                connection,
                server_hostname=hostname,
            ) as secure_socket:
                certificate = secure_socket.getpeercert()

        return {
            "enabled": True,
            "certificate_cn": _extract_common_name(
                certificate
            ),
            "certificate_expiration": (
                _extract_expiration_date(certificate)
            ),
        }

    except (OSError, ssl.SSLError, ValueError) as exc:
        return {
            "enabled": True,
            "certificate_cn": None,
            "certificate_expiration": None,
            "certificate_error": str(exc),
        }