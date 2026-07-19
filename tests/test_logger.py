import logging
from pathlib import Path

from utils.logger import setup_logging


def test_setup_logging_creates_log_file(
    tmp_path: Path,
) -> None:
    """
    Logging should write messages to the configured
    log file.
    """
    log_file = tmp_path / "test_recon.log"

    setup_logging(
        str(log_file)
    )

    logger = logging.getLogger(
        "test_logger"
    )

    logger.info(
        "Test log message"
    )

    logging.shutdown()

    assert log_file.exists()

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert "Test log message" in content
    assert "INFO" in content
    assert "test_logger" in content


def test_setup_logging_default_filename(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    The default log filename should be recon.log.
    """
    monkeypatch.chdir(
        tmp_path
    )

    setup_logging()

    logger = logging.getLogger(
        "default_logger"
    )

    logger.info(
        "Default log test"
    )

    logging.shutdown()

    log_file = tmp_path / "recon.log"

    assert log_file.exists()

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert "Default log test" in content