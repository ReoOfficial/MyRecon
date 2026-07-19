import re
from pathlib import Path

from utils.formatter import (
    print_report,
    print_report_location,
    print_report_save_error,
)


def strip_ansi(text: str) -> str:
    """
    Remove ANSI color codes from terminal output.
    """
    ansi_pattern = re.compile(
        r"\x1b\[[0-9;]*m"
    )

    return ansi_pattern.sub(
        "",
        text,
    )


def create_success_report(
    https_enabled: bool = True,
) -> dict:
    """
    Create a reusable successful scan report.
    """
    return {
        "input_target": "example.com",
        "success": True,
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 145.25,
        "headers": {
            "server": "nginx",
            "content_type": "text/html",
            "content_length": 1256,
        },
        "security_headers": {
            "Content-Security-Policy": True,
            "X-Frame-Options": False,
            "X-Content-Type-Options": True,
            "Strict-Transport-Security": False,
            "Referrer-Policy": True,
        },
        "redirects": {
            "detected": True,
            "count": 1,
            "final_url": "https://www.example.com",
        },
        "https": {
            "enabled": https_enabled,
            "certificate_cn": (
                "www.example.com"
                if https_enabled
                else None
            ),
            "certificate_expiration": (
                "2026-12-15T23:59:59+00:00"
                if https_enabled
                else None
            ),
        },
    }


def test_print_successful_report(
    capsys,
) -> None:
    """
    A successful report should display all
    collected information.
    """
    report = create_success_report()

    print_report(report)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "Target: example.com" in output
    assert "URL: https://example.com" in output
    assert "Status Code: 200" in output
    assert "Response Time: 145.25 ms" in output

    assert "Server: nginx" in output
    assert "Content-Type: text/html" in output
    assert "Content-Length: 1256" in output

    assert "Redirects Detected: Yes" in output
    assert "Redirect Count: 1" in output
    assert (
        "Final URL: https://www.example.com"
        in output
    )

    assert (
        "Content-Security-Policy: Present"
        in output
    )
    assert (
        "X-Frame-Options: Missing"
        in output
    )
    assert (
        "X-Content-Type-Options: Present"
        in output
    )
    assert (
        "Strict-Transport-Security: Missing"
        in output
    )
    assert (
        "Referrer-Policy: Present"
        in output
    )

    assert "HTTPS Enabled: Yes" in output
    assert (
        "Certificate CN: www.example.com"
        in output
    )
    assert (
        "Certificate Expiration: "
        "2026-12-15T23:59:59+00:00"
        in output
    )


def test_print_failed_report(
    capsys,
) -> None:
    """
    A failed scan should display the target
    and error reason.
    """
    report = {
        "input_target": "invalid.example",
        "success": False,
        "error": "Could not connect to the target.",
    }

    print_report(report)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "[ERROR] invalid.example" in output
    assert (
        "Reason: Could not connect to the target."
        in output
    )


def test_print_report_with_missing_values(
    capsys,
) -> None:
    """
    Missing optional HTTP values should be
    displayed as Not provided.
    """
    report = create_success_report()

    report["headers"] = {
        "server": None,
        "content_type": None,
        "content_length": None,
    }

    report["redirects"] = {
        "detected": False,
        "count": 0,
        "final_url": "https://example.com",
    }

    print_report(report)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "Server: Not provided" in output
    assert "Content-Type: Not provided" in output
    assert "Content-Length: Not provided" in output

    assert "Redirects Detected: No" in output
    assert "Redirect Count: 0" in output
    assert (
        "Final URL: https://example.com"
        in output
    )


def test_print_report_https_disabled(
    capsys,
) -> None:
    """
    HTTP targets should display HTTPS as disabled.
    """
    report = create_success_report(
        https_enabled=False
    )

    report["url"] = "http://example.com"

    print_report(report)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "HTTPS Enabled: No" in output

    assert "Certificate CN:" not in output
    assert "Certificate Expiration:" not in output


def test_print_report_missing_certificate_values(
    capsys,
) -> None:
    """
    Missing certificate values should display
    Not provided when HTTPS is enabled.
    """
    report = create_success_report()

    report["https"] = {
        "enabled": True,
        "certificate_cn": None,
        "certificate_expiration": None,
    }

    print_report(report)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "HTTPS Enabled: Yes" in output
    assert (
        "Certificate CN: Not provided"
        in output
    )
    assert (
        "Certificate Expiration: Not provided"
        in output
    )


def test_print_report_location(
    capsys,
) -> None:
    """
    The saved JSON report location should
    be displayed.
    """
    path = Path(
        "reports/recon_report.json"
    )

    print_report_location(path)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert "JSON report saved to:" in output
    assert str(path) in output


def test_print_report_save_error(
    capsys,
) -> None:
    """
    JSON save errors should be displayed.
    """
    error = OSError(
        "Permission denied"
    )

    print_report_save_error(error)

    captured = capsys.readouterr()
    output = strip_ansi(
        captured.out
    )

    assert (
        "Could not save JSON report"
        in output
    )
    assert "Permission denied" in output