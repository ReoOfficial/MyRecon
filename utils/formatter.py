from pathlib import Path

from colorama import Fore, Style, init


init(autoreset=True)


def _display_value(value: object) -> object:
    """
    Return a readable fallback for missing values.
    """
    if value is None or value == "":
        return "Not provided"

    return value


def print_report(report: dict) -> None:
    """
    Display a scan report in the terminal.
    """
    print()
    print(
        Style.BRIGHT
        + "=" * 60
    )

    target = report.get(
        "input_target",
        "Unknown target",
    )

    if not report.get("success"):
        print(
            Fore.RED
            + Style.BRIGHT
            + f"[ERROR] {target}"
        )
        print(
            Fore.RED
            + f"Reason: {report.get('error')}"
        )
        return

    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"[+] Target: {target}"
    )

    print(f"URL: {report['url']}")
    print(
        f"Status Code: "
        f"{report['status_code']}"
    )
    print(
        f"Response Time: "
        f"{report['response_time_ms']} ms"
    )

    headers = report["headers"]

    print()
    print(Style.BRIGHT + "HTTP Information")
    print(
        f"Server: "
        f"{_display_value(headers['server'])}"
    )
    print(
        f"Content-Type: "
        f"{_display_value(headers['content_type'])}"
    )
    print(
        f"Content-Length: "
        f"{_display_value(headers['content_length'])}"
    )

    redirects = report["redirects"]

    print()
    print(Style.BRIGHT + "Redirect Information")
    print(
        f"Redirects Detected: "
        f"{'Yes' if redirects['detected'] else 'No'}"
    )
    print(
        f"Redirect Count: "
        f"{redirects['count']}"
    )
    print(
        f"Final URL: "
        f"{redirects['final_url']}"
    )

    print()
    print(Style.BRIGHT + "Security Headers")

    for header, present in report[
        "security_headers"
    ].items():
        if present:
            print(
                Fore.GREEN
                + f"✅ {header}: Present"
            )
        else:
            print(
                Fore.RED
                + f"❌ {header}: Missing"
            )

    https_info = report["https"]

    print()
    print(Style.BRIGHT + "HTTPS Information")
    print(
        "HTTPS Enabled: "
        + (
            Fore.GREEN + "Yes"
            if https_info["enabled"]
            else Fore.RED + "No"
        )
    )

    if https_info["enabled"]:
        print(
            f"Certificate CN: "
            f"{_display_value(
                https_info['certificate_cn']
            )}"
        )
        print(
            f"Certificate Expiration: "
            f"{_display_value(
                https_info[
                    'certificate_expiration'
                ]
            )}"
        )


def print_report_location(
    path: Path,
) -> None:
    """
    Display the saved report location.
    """
    print()
    print(
        Fore.GREEN
        + Style.BRIGHT
        + f"[+] JSON report saved to: {path}"
    )


def print_report_save_error(
    error: Exception,
) -> None:
    """
    Display a JSON report saving error.
    """
    print()
    print(
        Fore.RED
        + Style.BRIGHT
        + "[ERROR] Could not save JSON report."
    )
    print(
        Fore.RED
        + f"Reason: {error}"
    )