import pytest

from security.headers import (
    SECURITY_HEADERS,
    check_security_headers,
)


def test_all_security_headers_present() -> None:
    """
    All required security headers should be detected.
    """
    headers = {
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Strict-Transport-Security": "max-age=31536000",
        "Referrer-Policy": "no-referrer",
    }

    result = check_security_headers(headers)

    assert result == {
        "Content-Security-Policy": True,
        "X-Frame-Options": True,
        "X-Content-Type-Options": True,
        "Strict-Transport-Security": True,
        "Referrer-Policy": True,
    }


def test_all_security_headers_missing() -> None:
    """
    All required security headers should be False
    when none are present.
    """
    result = check_security_headers({})

    assert result == {
        "Content-Security-Policy": False,
        "X-Frame-Options": False,
        "X-Content-Type-Options": False,
        "Strict-Transport-Security": False,
        "Referrer-Policy": False,
    }


@pytest.mark.parametrize(
    "present_header",
    SECURITY_HEADERS,
)
def test_individual_security_header_present(
    present_header: str,
) -> None:
    """
    Each required security header should be detected
    independently.
    """
    headers = {
        present_header: "test-value",
    }

    result = check_security_headers(headers)

    assert result[present_header] is True

    for header in SECURITY_HEADERS:
        if header != present_header:
            assert result[header] is False


def test_unrelated_headers_are_ignored() -> None:
    """
    Normal HTTP headers should not affect security
    header detection.
    """
    headers = {
        "Server": "nginx",
        "Content-Type": "text/html",
        "Cache-Control": "no-cache",
    }

    result = check_security_headers(headers)

    assert not any(result.values())