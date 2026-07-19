from unittest.mock import Mock, patch

import pytest

from core.request import send_get_request


def test_send_get_request_success() -> None:
    """
    A successful GET request should return the response
    and measured response time in milliseconds.
    """
    mock_client = Mock()
    mock_response = Mock()

    mock_client.get.return_value = mock_response

    with patch(
        "core.request.HttpClient",
        return_value=mock_client,
    ) as mock_client_class:
        with patch(
            "core.request.perf_counter",
            side_effect=[
                100.0,
                100.25,
            ],
        ):
            response, response_time_ms = (
                send_get_request(
                    "https://example.com",
                    timeout=5.0,
                )
            )

    mock_client_class.assert_called_once_with(
        timeout=5.0
    )

    mock_client.get.assert_called_once_with(
        "https://example.com"
    )

    mock_client.close.assert_called_once_with()

    assert response == mock_response
    assert response_time_ms == 250.0


def test_send_get_request_default_timeout() -> None:
    """
    The request function should use the default
    timeout of 10 seconds.
    """
    mock_client = Mock()
    mock_client.get.return_value = Mock()

    with patch(
        "core.request.HttpClient",
        return_value=mock_client,
    ) as mock_client_class:
        send_get_request(
            "https://example.com"
        )

    mock_client_class.assert_called_once_with(
        timeout=10.0
    )


def test_client_closes_when_request_fails() -> None:
    """
    The HTTP client should still be closed when
    the GET request raises an exception.
    """
    mock_client = Mock()

    mock_client.get.side_effect = (
        RuntimeError("Request failed")
    )

    with patch(
        "core.request.HttpClient",
        return_value=mock_client,
    ):
        with pytest.raises(
            RuntimeError,
            match="Request failed",
        ):
            send_get_request(
                "https://example.com"
            )

    mock_client.close.assert_called_once_with()