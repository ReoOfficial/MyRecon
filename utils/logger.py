import logging


def setup_logging(
    log_file: str = "recon.log",
) -> None:
    """
    Configure application logging.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        encoding="utf-8",
        force=True,
    )