import argparse


def build_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="MyRecon",
        description=(
            "Collect basic HTTP, security header, redirect, "
            "and HTTPS information from websites."
        ),
    )

    parser.add_argument(
        "targets",
        nargs="+",
        help="One or more domains or URLs to scan.",
    )

    return parser


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments provided by the user.
    """
    parser = build_parser()
    return parser.parse_args()