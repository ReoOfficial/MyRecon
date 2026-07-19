import ipaddress
import re
from urllib.parse import urlparse


DOMAIN_LABEL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
)


def _is_valid_hostname(hostname: str) -> bool:
    """
    Check whether a hostname is a valid domain name,
    localhost, or IP address.
    """
    if hostname == "localhost":
        return True

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        pass

    hostname = hostname.rstrip(".")

    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    if len(labels) < 2:
        return False

    return all(
        DOMAIN_LABEL_PATTERN.fullmatch(label)
        for label in labels
    )


def normalize_and_validate_target(target: str) -> str:
    """
    Normalize and validate a domain or URL.

    Examples:
        example.com -> https://example.com
        https://example.com -> https://example.com

    Raises:
        ValueError: If the target is invalid.
    """
    target = target.strip()

    if not target:
        raise ValueError("Target cannot be empty.")

    if any(character.isspace() for character in target):
        raise ValueError("Target cannot contain whitespace.")

    if "://" not in target:
        target = f"https://{target}"

    parsed_url = urlparse(target)

    if parsed_url.scheme not in ("http", "https"):
        raise ValueError(
            "Only HTTP and HTTPS URLs are supported."
        )

    if not parsed_url.hostname:
        raise ValueError("Target does not contain a valid hostname.")

    if not _is_valid_hostname(parsed_url.hostname):
        raise ValueError(
            f"Invalid hostname: {parsed_url.hostname}"
        )

    try:
        parsed_url.port
    except ValueError as exc:
        raise ValueError("Target contains an invalid port.") from exc

    return target