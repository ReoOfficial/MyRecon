import pytest

from cli.validator import normalize_and_validate_target


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        (
            "example.com",
            "https://example.com",
        ),
        (
            "https://example.com",
            "https://example.com",
        ),
        (
            "http://example.com",
            "http://example.com",
        ),
        (
            "sub.example.com/path",
            "https://sub.example.com/path",
        ),
        (
            "127.0.0.1",
            "https://127.0.0.1",
        ),
        (
            "localhost",
            "https://localhost",
        ),
    ],
)
def test_valid_targets(
    target: str,
    expected: str,
) -> None:
    """
    Valid targets should be normalized correctly.
    """
    result = normalize_and_validate_target(
        target
    )

    assert result == expected


@pytest.mark.parametrize(
    "target",
    [
        "",
        "   ",
        "hello world",
        "ftp://example.com",
        "example",
        "https://-example.com",
        "https://example..com",
        "https://example.com:99999",
    ],
)
def test_invalid_targets(
    target: str,
) -> None:
    """
    Invalid targets should raise ValueError.
    """
    with pytest.raises(ValueError):
        normalize_and_validate_target(
            target
        )


def test_hostname_too_long() -> None:
    """
    Hostnames longer than 253 characters
    should be rejected.
    """
    long_hostname = ".".join(
        [
            "a" * 63,
            "b" * 63,
            "c" * 63,
            "d" * 63,
        ]
    )

    with pytest.raises(
        ValueError,
        match="Invalid hostname",
    ):
        normalize_and_validate_target(
            f"https://{long_hostname}"
        )


def test_url_without_hostname() -> None:
    """
    A URL without a hostname should be rejected.
    """
    with pytest.raises(
        ValueError,
        match=(
            "Target does not contain "
            "a valid hostname"
        ),
    ):
        normalize_and_validate_target(
            "https://"
        )