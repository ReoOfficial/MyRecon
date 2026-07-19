from unittest.mock import Mock, patch

from core.client import HttpClient


@patch("core.client.requests.Session")
def test_client_initialization(
    mock_session_class: Mock,
) -> None:
    """
    HttpClient should create a requests Session,
    store the timeout, and configure the User-Agent.
    """
    mock_session = Mock()
    mock_session_class.return_value = mock_session

    client = HttpClient(
        timeout=5.0,
    )

    assert client.timeout == 5.0
    assert client.session == mock_session

    mock_session.headers.update.assert_called_once_with(
        {
            "User-Agent": "MyRecon/1.0",
        }
    )


@patch("core.client.requests.Session")
def test_client_default_timeout(
    mock_session_class: Mock,
) -> None:
    """
    HttpClient should use a default timeout of
    10 seconds.
    """
    mock_session = Mock()
    mock_session_class.return_value = mock_session

    client = HttpClient()

    assert client.timeout == 10.0


@patch("core.client.requests.Session")
def test_get_request(
    mock_session_class: Mock,
) -> None:
    """
    The GET method should send a request using
    the configured timeout and follow redirects.
    """
    mock_session = Mock()
    mock_response = Mock()

    mock_session_class.return_value = mock_session
    mock_session.get.return_value = mock_response

    client = HttpClient(
        timeout=7.5,
    )

    result = client.get(
        "https://example.com"
    )

    mock_session.get.assert_called_once_with(
        "https://example.com",
        timeout=7.5,
        allow_redirects=True,
    )

    assert result == mock_response


@patch("core.client.requests.Session")
def test_close_client(
    mock_session_class: Mock,
) -> None:
    """
    Closing the client should close the
    underlying requests Session.
    """
    mock_session = Mock()
    mock_session_class.return_value = mock_session

    client = HttpClient()

    client.close()

    mock_session.close.assert_called_once_with()