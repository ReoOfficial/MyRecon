from unittest.mock import MagicMock, patch

from security.certificate import (
    _extract_common_name,
    _extract_expiration_date,
    get_https_information,
)


def test_extract_common_name() -> None:
    """
    The certificate Common Name should be extracted
    from the subject field.
    """
    certificate = {
        "subject": (
            (
                ("commonName", "example.com"),
            ),
        )
    }

    result = _extract_common_name(
        certificate
    )

    assert result == "example.com"


def test_extract_common_name_missing() -> None:
    """
    None should be returned when no Common Name exists.
    """
    certificate = {
        "subject": (
            (
                (
                    "organizationName",
                    "Example Inc.",
                ),
            ),
        )
    }

    result = _extract_common_name(
        certificate
    )

    assert result is None


def test_extract_common_name_without_subject() -> None:
    """
    A certificate without a subject should return None.
    """
    result = _extract_common_name({})

    assert result is None


@patch(
    "security.certificate.ssl.cert_time_to_seconds",
    return_value=1797379199.0,
)
def test_extract_expiration_date(
    mock_cert_time: MagicMock,
) -> None:
    """
    The certificate expiration date should be
    converted to an ISO formatted UTC datetime.
    """
    certificate = {
        "notAfter": "Dec 15 23:59:59 2026 GMT",
    }

    result = _extract_expiration_date(
        certificate
    )

    assert result is not None
    assert result.endswith("+00:00")

    mock_cert_time.assert_called_once_with(
        "Dec 15 23:59:59 2026 GMT"
    )


def test_extract_expiration_date_missing() -> None:
    """
    None should be returned when the certificate
    has no expiration date.
    """
    result = _extract_expiration_date({})

    assert result is None


def test_http_target_has_no_https_information() -> None:
    """
    HTTP targets should report HTTPS as disabled.
    """
    result = get_https_information(
        "http://example.com"
    )

    assert result == {
        "enabled": False,
        "certificate_cn": None,
        "certificate_expiration": None,
    }


def test_https_target_without_hostname() -> None:
    """
    An HTTPS URL without a hostname should return
    certificate information as unavailable.
    """
    result = get_https_information(
        "https://"
    )

    assert result == {
        "enabled": True,
        "certificate_cn": None,
        "certificate_expiration": None,
        "certificate_error": "Hostname unavailable.",
    }


@patch(
    "security.certificate.ssl.create_default_context"
)
@patch(
    "security.certificate.socket.create_connection"
)
def test_https_certificate_success(
    mock_create_connection: MagicMock,
    mock_create_context: MagicMock,
) -> None:
    """
    Valid HTTPS certificate information should
    be extracted successfully.
    """
    mock_connection = MagicMock()
    mock_secure_socket = MagicMock()
    mock_context = MagicMock()

    mock_create_connection.return_value = (
        mock_connection
    )

    mock_create_context.return_value = (
        mock_context
    )

    mock_context.wrap_socket.return_value = (
        mock_secure_socket
    )

    mock_secure_socket.__enter__.return_value.getpeercert.return_value = {
        "subject": (
            (
                (
                    "commonName",
                    "example.com",
                ),
            ),
        ),
        "notAfter": (
            "Dec 15 23:59:59 2026 GMT"
        ),
    }

    result = get_https_information(
        "https://example.com"
    )

    assert result["enabled"] is True
    assert (
        result["certificate_cn"]
        == "example.com"
    )

    assert (
        result["certificate_expiration"]
        is not None
    )

    mock_create_connection.assert_called_once_with(
        (
            "example.com",
            443,
        ),
        timeout=5.0,
    )

    mock_context.wrap_socket.assert_called_once()

    call_args = (
        mock_context.wrap_socket.call_args
    )

    assert (
        call_args.kwargs["server_hostname"]
        == "example.com"
    )


@patch(
    "security.certificate.ssl.create_default_context"
)
@patch(
    "security.certificate.socket.create_connection"
)
def test_https_custom_port(
    mock_create_connection: MagicMock,
    mock_create_context: MagicMock,
) -> None:
    """
    A custom HTTPS port should be used when provided.
    """
    mock_connection = MagicMock()
    mock_secure_socket = MagicMock()
    mock_context = MagicMock()

    mock_create_connection.return_value = (
        mock_connection
    )

    mock_create_context.return_value = (
        mock_context
    )

    mock_context.wrap_socket.return_value = (
        mock_secure_socket
    )

    mock_secure_socket.__enter__.return_value.getpeercert.return_value = {}

    get_https_information(
        "https://example.com:8443"
    )

    mock_create_connection.assert_called_once_with(
        (
            "example.com",
            8443,
        ),
        timeout=5.0,
    )


@patch(
    "security.certificate.ssl.create_default_context"
)
@patch(
    "security.certificate.socket.create_connection"
)
def test_https_connection_error(
    mock_create_connection: MagicMock,
    mock_create_context: MagicMock,
) -> None:
    """
    Network errors during certificate inspection
    should not crash the application.
    """
    mock_create_connection.side_effect = (
        OSError("Connection failed")
    )

    result = get_https_information(
        "https://example.com"
    )

    assert result == {
        "enabled": True,
        "certificate_cn": None,
        "certificate_expiration": None,
        "certificate_error": "Connection failed",
    }