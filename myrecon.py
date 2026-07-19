import logging

from cli.parser import parse_arguments
from core.scanner import scan_targets
from reporting.json_report import save_json_report
from utils.formatter import (
    print_report,
    print_report_location,
    print_report_save_error,
)
from utils.logger import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    """
    Run the MyRecon command-line application.
    """
    setup_logging()

    args = parse_arguments()

    reports = scan_targets(
        args.targets
    )

    for report in reports:
        print_report(report)

    try:
        report_path = save_json_report(
            reports
        )

        print_report_location(
            report_path
        )

    except OSError as exc:
        logger.exception(
            "Could not save JSON report."
        )

        print_report_save_error(
            exc
        )


if __name__ == "__main__":
    main()