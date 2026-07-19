import runpy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import myrecon


def test_main_success() -> None:
    """
    The main application should scan targets,
    print reports, and save the JSON report.
    """
    args = SimpleNamespace(
        targets=[
            "example.com",
        ]
    )

    reports = [
        {
            "input_target": "example.com",
            "success": True,
        }
    ]

    report_path = Path(
        "reports/recon_report.json"
    )

    with patch(
        "myrecon.setup_logging"
    ) as mock_setup_logging:
        with patch(
            "myrecon.parse_arguments",
            return_value=args,
        ) as mock_parse_arguments:
            with patch(
                "myrecon.scan_targets",
                return_value=reports,
            ) as mock_scan_targets:
                with patch(
                    "myrecon.print_report"
                ) as mock_print_report:
                    with patch(
                        "myrecon.save_json_report",
                        return_value=report_path,
                    ) as mock_save_report:
                        with patch(
                            "myrecon.print_report_location"
                        ) as mock_print_location:
                            myrecon.main()

    mock_setup_logging.assert_called_once_with()

    mock_parse_arguments.assert_called_once_with()

    mock_scan_targets.assert_called_once_with(
        [
            "example.com",
        ]
    )

    mock_print_report.assert_called_once_with(
        reports[0]
    )

    mock_save_report.assert_called_once_with(
        reports
    )

    mock_print_location.assert_called_once_with(
        report_path
    )


def test_main_prints_multiple_reports() -> None:
    """
    The main application should print every
    returned scan report.
    """
    args = SimpleNamespace(
        targets=[
            "example.com",
            "github.com",
        ]
    )

    reports = [
        {
            "input_target": "example.com",
            "success": True,
        },
        {
            "input_target": "github.com",
            "success": True,
        },
    ]

    report_path = Path(
        "reports/recon_report.json"
    )

    with patch(
        "myrecon.setup_logging"
    ):
        with patch(
            "myrecon.parse_arguments",
            return_value=args,
        ):
            with patch(
                "myrecon.scan_targets",
                return_value=reports,
            ):
                with patch(
                    "myrecon.print_report"
                ) as mock_print_report:
                    with patch(
                        "myrecon.save_json_report",
                        return_value=report_path,
                    ):
                        with patch(
                            "myrecon.print_report_location"
                        ):
                            myrecon.main()

    assert mock_print_report.call_count == 2

    mock_print_report.assert_any_call(
        reports[0]
    )

    mock_print_report.assert_any_call(
        reports[1]
    )


def test_main_handles_json_save_error() -> None:
    """
    JSON saving errors should be logged and
    displayed without crashing the application.
    """
    args = SimpleNamespace(
        targets=[
            "example.com",
        ]
    )

    reports = [
        {
            "input_target": "example.com",
            "success": True,
        }
    ]

    error = OSError(
        "Permission denied"
    )

    with patch(
        "myrecon.setup_logging"
    ):
        with patch(
            "myrecon.parse_arguments",
            return_value=args,
        ):
            with patch(
                "myrecon.scan_targets",
                return_value=reports,
            ):
                with patch(
                    "myrecon.print_report"
                ):
                    with patch(
                        "myrecon.save_json_report",
                        side_effect=error,
                    ):
                        with patch(
                            "myrecon.logger.exception"
                        ) as mock_logger:
                            with patch(
                                "myrecon.print_report_save_error"
                            ) as mock_print_error:
                                myrecon.main()

    mock_logger.assert_called_once_with(
        "Could not save JSON report."
    )

    mock_print_error.assert_called_once_with(
        error
    )


def test_myrecon_script_entry_point() -> None:
    """
    Running myrecon.py as a script should execute
    the main application entry point.
    """
    project_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    script_path = (
        project_root
        / "myrecon.py"
    )

    args = SimpleNamespace(
        targets=[]
    )

    report_path = Path(
        "reports/recon_report.json"
    )

    with patch(
        "utils.logger.setup_logging"
    ) as mock_setup_logging:
        with patch(
            "cli.parser.parse_arguments",
            return_value=args,
        ):
            with patch(
                "core.scanner.scan_targets",
                return_value=[],
            ):
                with patch(
                    "reporting.json_report.save_json_report",
                    return_value=report_path,
                ):
                    with patch(
                        "utils.formatter.print_report"
                    ):
                        with patch(
                            "utils.formatter.print_report_location"
                        ):
                            runpy.run_path(
                                str(script_path),
                                run_name="__main__",
                            )

    mock_setup_logging.assert_called_once_with()