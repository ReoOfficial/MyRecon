import logging
from concurrent.futures import ThreadPoolExecutor

import requests

from cli.validator import normalize_and_validate_target
from core.request import send_get_request
from core.response import analyze_response
from security.certificate import get_https_information
from security.headers import check_security_headers


logger = logging.getLogger(__name__)

MAX_WORKERS = 5


def _build_error_report(
    target: str,
    error: str,
) -> dict:
    """
    Build a structured report for a failed target.
    """
    return {
        "input_target": target,
        "success": False,
        "error": error,
    }


def scan_target(target: str) -> dict:
    """
    Scan a single target and return a structured report.
    """
    logger.info(
        "Starting scan for target: %s",
        target,
    )

    try:
        url = normalize_and_validate_target(
            target
        )

        response, response_time_ms = (
            send_get_request(url)
        )

        response_data = analyze_response(
            response,
            response_time_ms,
        )

        security_headers = (
            check_security_headers(
                response.headers
            )
        )

        final_url = response_data[
            "redirects"
        ]["final_url"]

        https_information = (
            get_https_information(
                final_url
            )
        )

        report = {
            "input_target": target,
            "success": True,
            "url": url,
            "status_code": response_data[
                "status_code"
            ],
            "response_time_ms": response_data[
                "response_time_ms"
            ],
            "headers": response_data[
                "headers"
            ],
            "security_headers": (
                security_headers
            ),
            "redirects": response_data[
                "redirects"
            ],
            "https": https_information,
        }

        logger.info(
            "Scan completed successfully for: %s",
            target,
        )

        return report

    except ValueError as exc:
        message = str(exc)

        logger.warning(
            "Validation failed for %s: %s",
            target,
            message,
        )

        return _build_error_report(
            target,
            message,
        )

    except requests.exceptions.Timeout:
        message = "The request timed out."

        logger.error(
            "Request timed out for: %s",
            target,
        )

        return _build_error_report(
            target,
            message,
        )

    except requests.exceptions.ConnectionError:
        message = (
            "Could not connect to the target."
        )

        logger.error(
            "Connection failed for: %s",
            target,
        )

        return _build_error_report(
            target,
            message,
        )

    except requests.exceptions.RequestException as exc:
        message = (
            f"HTTP request failed: {exc}"
        )

        logger.error(
            "HTTP request failed for %s: %s",
            target,
            exc,
        )

        return _build_error_report(
            target,
            message,
        )

    except Exception as exc:
        logger.exception(
            "Unexpected error while scanning %s",
            target,
        )

        return _build_error_report(
            target,
            f"Unexpected error: {exc}",
        )


def scan_targets(
    targets: list[str],
) -> list[dict]:
    """
    Scan one or more targets.

    Multiple targets are scanned concurrently using
    ThreadPoolExecutor.
    """
    if not targets:
        return []

    if len(targets) == 1:
        return [
            scan_target(targets[0])
        ]

    worker_count = min(
        MAX_WORKERS,
        len(targets),
    )

    logger.info(
        "Starting concurrent scan of %s targets "
        "using %s workers.",
        len(targets),
        worker_count,
    )

    with ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        reports = list(
            executor.map(
                scan_target,
                targets,
            )
        )

    return reports