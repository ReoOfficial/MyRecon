import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_json_report(
    reports: list[dict],
    output_path: str = "reports/recon_report.json",
) -> Path:
    """
    Save all scan results into a JSON report.
    """
    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_data = {
        "target_count": len(reports),
        "results": reports,
    }

    with path.open(
        "w",
        encoding="utf-8",
    ) as report_file:
        json.dump(
            report_data,
            report_file,
            indent=4,
            ensure_ascii=False,
        )

    logger.info(
        "JSON report saved to %s",
        path,
    )

    return path