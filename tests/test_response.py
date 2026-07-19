from unittest.mock import Mock

from core.response import analyze_response


def create_mock_response(
    status_code: int = 200,
    headers: dict | None = None,
    url: str = "https://example.com",
    history: list | None = None,
) -> Mock:
    """
    Create a mock requests.Response object.
    """
    response = Mock()

    response.status_code = status_code
    response.headers = headers or {}
    response.url = url
    response.history = history or []

    return response


def test_analyze_response_with_all_headers() -> None:
    """
    Response information should be extracted correctly.
    """
    response = create_mock_response(
        status_code=200,
        headers={
            "Server": "nginx",
            "Content-Type": "text/html",
            "Content-Length": "1256",
        },
    )

    result = analyze_response(
        response,
        145.25,
    )

    assert result == {
        "status_code": 200,
        "response_time_ms": 145.25,
        "headers": {
            "server": "nginx",
            "content_type": "text/html",
            "content_length": 1256,
        },
        "redirects": {
            "detected": False,
            "count": 0,
            "final_url": "https://example.com",
        },
    }


def test_analyze_response_with_missing_headers() -> None:
    """
    Missing optional headers should return None.
    """
    response = create_mock_response()

    result = analyze_response(
        response,
        100.0,
    )

    assert result["headers"] == {
        "server": None,
        "content_type": None,
        "content_length": None,
    }


def test_content_length_invalid_value() -> None:
    """
    A non-numeric Content-Length should be preserved
    instead of causing an error.
    """
    response = create_mock_response(
        headers={
            "Content-Length": "unknown",
        }
    )

    result = analyze_response(
        response,
        50.0,
    )

    assert (
        result["headers"]["content_length"]
        == "unknown"
    )


def test_redirect_detection() -> None:
    """
    Redirect history and final destination should
    be reported correctly.
    """
    redirect_one = Mock()
    redirect_two = Mock()

    response = create_mock_response(
        url="https://www.example.com/final",
        history=[
            redirect_one,
            redirect_two,
        ],
    )

    result = analyze_response(
        response,
        200.0,
    )

    assert result["redirects"] == {
        "detected": True,
        "count": 2,
        "final_url": (
            "https://www.example.com/final"
        ),
    }


def test_different_status_code() -> None:
    """
    HTTP status codes should be preserved.
    """
    response = create_mock_response(
        status_code=404,
    )

    result = analyze_response(
        response,
        75.5,
    )

    assert result["status_code"] == 404
    assert result["response_time_ms"] == 75.5