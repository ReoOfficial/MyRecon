from unittest.mock import Mock, patch

import requests

from core.scanner import (
    scan_target,
    scan_targets,
)


@patch(
    "core.scanner.get_https_information"
)
@patch(
    "core.scanner.check_security_headers"
)
@patch(
    "core.scanner.analyze_response"
)
@patch(
    "core.scanner.send_get_request"
)
@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_success(
    mock_validate: Mock,
    mock_send_request: Mock,
    mock_analyze_response: Mock,
    mock_check_headers: Mock,
    mock_https_info: Mock,
) -> None:
    """
    A valid target should return a complete
    successful scan report.
    """
    mock_response = Mock()

    mock_validate.return_value = (
        "https://example.com"
    )

    mock_send_request.return_value = (
        mock_response,
        150.5,
    )

    mock_analyze_response.return_value = {
        "status_code": 200,
        "response_time_ms": 150.5,
        "headers": {
            "server": "nginx",
            "content_type": "text/html",
            "content_length": 1256,
        },
        "redirects": {
            "detected": True,
            "count": 1,
            "final_url": (
                "https://www.example.com"
            ),
        },
    }

    mock_check_headers.return_value = {
        "Content-Security-Policy": True,
        "X-Frame-Options": False,
        "X-Content-Type-Options": True,
        "Strict-Transport-Security": True,
        "Referrer-Policy": False,
    }

    mock_https_info.return_value = {
        "enabled": True,
        "certificate_cn": "www.example.com",
        "certificate_expiration": (
            "2026-12-15T23:59:59+00:00"
        ),
    }

    result = scan_target(
        "example.com"
    )

    assert result == {
        "input_target": "example.com",
        "success": True,
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 150.5,
        "headers": {
            "server": "nginx",
            "content_type": "text/html",
            "content_length": 1256,
        },
        "security_headers": {
            "Content-Security-Policy": True,
            "X-Frame-Options": False,
            "X-Content-Type-Options": True,
            "Strict-Transport-Security": True,
            "Referrer-Policy": False,
        },
        "redirects": {
            "detected": True,
            "count": 1,
            "final_url": (
                "https://www.example.com"
            ),
        },
        "https": {
            "enabled": True,
            "certificate_cn": (
                "www.example.com"
            ),
            "certificate_expiration": (
                "2026-12-15T23:59:59+00:00"
            ),
        },
    }

    mock_validate.assert_called_once_with(
        "example.com"
    )

    mock_send_request.assert_called_once_with(
        "https://example.com"
    )

    mock_analyze_response.assert_called_once_with(
        mock_response,
        150.5,
    )

    mock_check_headers.assert_called_once_with(
        mock_response.headers
    )

    # HTTPS information must use the final URL
    # after redirects.
    mock_https_info.assert_called_once_with(
        "https://www.example.com"
    )


@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_validation_error(
    mock_validate: Mock,
) -> None:
    """
    Validation errors should return a failed
    report instead of crashing.
    """
    mock_validate.side_effect = ValueError(
        "Invalid hostname."
    )

    result = scan_target(
        "invalid"
    )

    assert result == {
        "input_target": "invalid",
        "success": False,
        "error": "Invalid hostname.",
    }


@patch(
    "core.scanner.send_get_request"
)
@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_timeout(
    mock_validate: Mock,
    mock_send_request: Mock,
) -> None:
    """
    Request timeouts should be handled safely.
    """
    mock_validate.return_value = (
        "https://example.com"
    )

    mock_send_request.side_effect = (
        requests.exceptions.Timeout()
    )

    result = scan_target(
        "example.com"
    )

    assert result == {
        "input_target": "example.com",
        "success": False,
        "error": "The request timed out.",
    }


@patch(
    "core.scanner.send_get_request"
)
@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_connection_error(
    mock_validate: Mock,
    mock_send_request: Mock,
) -> None:
    """
    Connection errors should be handled safely.
    """
    mock_validate.return_value = (
        "https://example.com"
    )

    mock_send_request.side_effect = (
        requests.exceptions.ConnectionError()
    )

    result = scan_target(
        "example.com"
    )

    assert result == {
        "input_target": "example.com",
        "success": False,
        "error": (
            "Could not connect to the target."
        ),
    }


@patch(
    "core.scanner.send_get_request"
)
@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_request_exception(
    mock_validate: Mock,
    mock_send_request: Mock,
) -> None:
    """
    General requests exceptions should return
    a failed report.
    """
    mock_validate.return_value = (
        "https://example.com"
    )

    mock_send_request.side_effect = (
        requests.exceptions.RequestException(
            "Request failed"
        )
    )

    result = scan_target(
        "example.com"
    )

    assert result == {
        "input_target": "example.com",
        "success": False,
        "error": (
            "HTTP request failed: Request failed"
        ),
    }


@patch(
    "core.scanner.send_get_request"
)
@patch(
    "core.scanner.normalize_and_validate_target"
)
def test_scan_target_unexpected_exception(
    mock_validate: Mock,
    mock_send_request: Mock,
) -> None:
    """
    Unexpected exceptions should be caught so
    one failed target cannot stop the program.
    """
    mock_validate.return_value = (
        "https://example.com"
    )

    mock_send_request.side_effect = (
        RuntimeError(
            "Something unexpected happened"
        )
    )

    result = scan_target(
        "example.com"
    )

    assert result == {
        "input_target": "example.com",
        "success": False,
        "error": (
            "Unexpected error: "
            "Something unexpected happened"
        ),
    }


def test_scan_targets_empty_list() -> None:
    """
    An empty target list should return an
    empty report list.
    """
    result = scan_targets([])

    assert result == []


@patch(
    "core.scanner.scan_target"
)
def test_scan_targets_single_target(
    mock_scan_target: Mock,
) -> None:
    """
    A single target should be scanned directly
    without requiring concurrent execution.
    """
    mock_report = {
        "input_target": "example.com",
        "success": True,
    }

    mock_scan_target.return_value = (
        mock_report
    )

    result = scan_targets(
        [
            "example.com",
        ]
    )

    assert result == [
        mock_report,
    ]

    mock_scan_target.assert_called_once_with(
        "example.com"
    )


@patch(
    "core.scanner.scan_target"
)
def test_scan_targets_multiple_targets(
    mock_scan_target: Mock,
) -> None:
    """
    Multiple targets should all be scanned and
    returned in the original target order.
    """
    targets = [
        "example.com",
        "github.com",
        "openai.com",
    ]

    def fake_scan(
        target: str,
    ) -> dict:
        return {
            "input_target": target,
            "success": True,
        }

    mock_scan_target.side_effect = (
        fake_scan
    )

    result = scan_targets(
        targets
    )

    assert result == [
        {
            "input_target": "example.com",
            "success": True,
        },
        {
            "input_target": "github.com",
            "success": True,
        },
        {
            "input_target": "openai.com",
            "success": True,
        },
    ]

    assert mock_scan_target.call_count == 3