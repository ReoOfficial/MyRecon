from requests import Response


def _parse_content_length(
    content_length: str | None,
) -> int | str | None:
    """
    Convert Content-Length to an integer when possible.
    """
    if content_length is None:
        return None

    try:
        return int(content_length)
    except ValueError:
        return content_length


def analyze_response(
    response: Response,
    response_time_ms: float,
) -> dict:
    """
    Extract relevant information from an HTTP response.
    """
    return {
        "status_code": response.status_code,
        "response_time_ms": response_time_ms,
        "headers": {
            "server": response.headers.get("Server"),
            "content_type": response.headers.get(
                "Content-Type"
            ),
            "content_length": _parse_content_length(
                response.headers.get("Content-Length")
            ),
        },
        "redirects": {
            "detected": bool(response.history),
            "count": len(response.history),
            "final_url": response.url,
        },
    }