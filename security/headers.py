from collections.abc import Mapping


SECURITY_HEADERS = (
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy",
)


def check_security_headers(
    headers: Mapping[str, str],
) -> dict[str, bool]:
    """
    Check whether required security headers are present.
    """
    return {
        header: header in headers
        for header in SECURITY_HEADERS
    }