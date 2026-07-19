import sys

import pytest

from cli.parser import parse_arguments


def test_single_target(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The parser should accept a single target.
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "myrecon.py",
            "example.com",
        ],
    )

    args = parse_arguments()

    assert args.targets == [
        "example.com",
    ]


def test_multiple_targets(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The parser should accept multiple targets.
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "myrecon.py",
            "google.com",
            "github.com",
            "openai.com",
        ],
    )

    args = parse_arguments()

    assert args.targets == [
        "google.com",
        "github.com",
        "openai.com",
    ]


def test_full_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The parser should accept a full URL.
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "myrecon.py",
            "https://example.com",
        ],
    )

    args = parse_arguments()

    assert args.targets == [
        "https://example.com",
    ]


def test_no_targets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    The parser should exit when no target is provided.
    """
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "myrecon.py",
        ],
    )

    with pytest.raises(SystemExit):
        parse_arguments()