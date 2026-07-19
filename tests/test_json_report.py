import json
from pathlib import Path
from unittest.mock import patch

import pytest

from reporting.json_report import save_json_report


def test_save_json_report(
    tmp_path: Path,
) -> None:
    """
    Scan reports should be saved as valid JSON.
    """
    reports = [
        {
            "input_target": "example.com",
            "success": True,
            "status_code": 200,
        }
    ]

    output_path = (
        tmp_path
        / "reports"
        / "recon_report.json"
    )

    result = save_json_report(
        reports,
        str(output_path),
    )

    assert result == output_path
    assert output_path.exists()

    with output_path.open(
        "r",
        encoding="utf-8",
    ) as report_file:
        saved_data = json.load(
            report_file
        )

    assert saved_data == {
        "target_count": 1,
        "results": reports,
    }


def test_save_multiple_reports(
    tmp_path: Path,
) -> None:
    """
    Multiple target reports should be saved
    in the same JSON report.
    """
    reports = [
        {
            "input_target": "example.com",
            "success": True,
        },
        {
            "input_target": "github.com",
            "success": True,
        },
        {
            "input_target": "invalid.com",
            "success": False,
            "error": "Connection failed",
        },
    ]

    output_path = (
        tmp_path
        / "recon_report.json"
    )

    save_json_report(
        reports,
        str(output_path),
    )

    with output_path.open(
        "r",
        encoding="utf-8",
    ) as report_file:
        saved_data = json.load(
            report_file
        )

    assert saved_data["target_count"] == 3
    assert saved_data["results"] == reports


def test_save_empty_report_list(
    tmp_path: Path,
) -> None:
    """
    An empty report list should still produce
    valid JSON.
    """
    output_path = (
        tmp_path
        / "empty_report.json"
    )

    save_json_report(
        [],
        str(output_path),
    )

    with output_path.open(
        "r",
        encoding="utf-8",
    ) as report_file:
        saved_data = json.load(
            report_file
        )

    assert saved_data == {
        "target_count": 0,
        "results": [],
    }


def test_parent_directory_is_created(
    tmp_path: Path,
) -> None:
    """
    Missing parent directories should be
    created automatically.
    """
    output_path = (
        tmp_path
        / "new"
        / "nested"
        / "directory"
        / "report.json"
    )

    assert not output_path.parent.exists()

    save_json_report(
        [],
        str(output_path),
    )

    assert output_path.parent.exists()
    assert output_path.exists()


def test_json_report_filesystem_error() -> None:
    """
    Filesystem errors should propagate so the
    application can handle them.
    """
    reports = [
        {
            "input_target": "example.com",
        }
    ]

    with patch(
        "reporting.json_report.Path.mkdir",
        side_effect=OSError(
            "Permission denied"
        ),
    ):
        with pytest.raises(
            OSError,
            match="Permission denied",
        ):
            save_json_report(
                reports
            )