# MyRecon

MyRecon is a modular Python command-line web reconnaissance tool that collects basic HTTP, security header, redirect, and HTTPS certificate information from one or more websites.

The project was designed with separation of responsibilities in mind, with individual modules handling command-line parsing, input validation, HTTP communication, response analysis, security checks, certificate inspection, reporting, formatting, logging, and concurrent scanning.

## Features

MyRecon supports:

* Domain and full URL input
* Automatic HTTPS normalization
* Input validation before requests are sent
* HTTP GET requests
* HTTP status code detection
* Response time measurement in milliseconds
* Server header detection
* Content-Type detection
* Content-Length detection when available
* HTTP redirect detection
* Redirect count reporting
* Final destination URL detection
* Common HTTP security header checks
* HTTPS detection
* SSL/TLS certificate Common Name extraction
* SSL/TLS certificate expiration date extraction
* Multiple target scanning
* Concurrent scanning with `ThreadPoolExecutor`
* Colored terminal output with `colorama`
* Structured JSON report generation
* Application and error logging
* Graceful error handling
* Automated testing with `pytest`
* Test coverage reporting with `pytest-cov`

## Security Headers

MyRecon checks whether the following HTTP response headers are present:

* `Content-Security-Policy`
* `X-Frame-Options`
* `X-Content-Type-Options`
* `Strict-Transport-Security`
* `Referrer-Policy`

Each header is displayed as either:

```text
✅ Present
```

or:

```text
❌ Missing
```

MyRecon checks whether these headers are present but does not currently evaluate whether their individual configurations are secure.

## Project Structure

```text
MyRecon/
│
├── myrecon.py
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
│
├── cli/
│   ├── __init__.py
│   ├── parser.py
│   └── validator.py
│
├── core/
│   ├── __init__.py
│   ├── client.py
│   ├── request.py
│   ├── response.py
│   └── scanner.py
│
├── reporting/
│   ├── __init__.py
│   └── json_report.py
│
├── security/
│   ├── __init__.py
│   ├── certificate.py
│   └── headers.py
│
├── utils/
│   ├── __init__.py
│   ├── formatter.py
│   └── logger.py
│
├── reports/
│
└── tests/
    ├── __init__.py
    ├── test_certificate.py
    ├── test_client.py
    ├── test_formatter.py
    ├── test_headers.py
    ├── test_json_report.py
    ├── test_logger.py
    ├── test_myrecon.py
    ├── test_parser.py
    ├── test_request.py
    ├── test_response.py
    ├── test_scanner.py
    └── test_validator.py
```

## Architecture

The application follows the following general flow:

```text
myrecon.py
    ↓
CLI Parser
    ↓
Target Validation
    ↓
Scanner
    ↓
HTTP Client / Request
    ↓
Response Analysis
    ↓
Security Header Check
    ↓
HTTPS Certificate Inspection
    ↓
Terminal Output
    ↓
JSON Report
```

### `cli`

Handles command-line input and target validation.

### `core`

Contains the main HTTP and scanning functionality.

### `security`

Handles HTTP security header checks and HTTPS certificate inspection.

### `reporting`

Handles structured JSON report generation.

### `utils`

Handles terminal formatting and application logging.

### `tests`

Contains the automated test suite for the project.

## Requirements

MyRecon requires Python 3.10 or newer.

Runtime dependencies:

* `requests`
* `colorama`

Development dependencies:

* `pytest`
* `pytest-cov`

The project also uses Python standard library modules including:

* `argparse`
* `urllib.parse`
* `json`
* `logging`
* `concurrent.futures`
* `ssl`
* `socket`
* `ipaddress`

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd MyRecon
```

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the runtime dependencies:

```bash
pip install -r requirements.txt
```

For development and testing, install:

```bash
pip install -r requirements-dev.txt
```

## Usage

Scan a single domain:

```bash
python myrecon.py example.com
```

Scan a full URL:

```bash
python myrecon.py https://example.com
```

Scan multiple targets:

```bash
python myrecon.py google.com github.com openai.com
```

When a target is provided without an HTTP or HTTPS scheme, MyRecon automatically adds HTTPS.

For example:

```text
example.com
```

is normalized to:

```text
https://example.com
```

## Example Output

```text
============================================================
[+] Target: example.com
URL: https://example.com
Status Code: 200
Response Time: 145.25 ms

HTTP Information
Server: nginx
Content-Type: text/html
Content-Length: 1256

Redirect Information
Redirects Detected: Yes
Redirect Count: 1
Final URL: https://www.example.com/

Security Headers
✅ Content-Security-Policy: Present
❌ X-Frame-Options: Missing
✅ X-Content-Type-Options: Present
✅ Strict-Transport-Security: Present
❌ Referrer-Policy: Missing

HTTPS Information
HTTPS Enabled: Yes
Certificate CN: www.example.com
Certificate Expiration: 2026-12-15T23:59:59+00:00
```

Actual results depend on the target website.

## Redirect Detection

MyRecon follows HTTP redirects and reports:

* Whether redirects were detected
* The number of redirects
* The final destination URL

For example:

```text
Requested URL:
https://google.com

Redirect Count:
1

Final URL:
https://www.google.com/
```

## HTTPS Certificate Information

For HTTPS targets, MyRecon attempts to retrieve:

* Whether HTTPS is enabled
* Certificate Common Name (CN)
* Certificate expiration date

Certificate inspection failures are handled gracefully and do not stop the rest of the scan.

## Multiple Target Scanning

Multiple targets can be provided in a single command:

```bash
python myrecon.py example.com github.com openai.com
```

MyRecon uses Python's `ThreadPoolExecutor` to scan multiple targets concurrently.

A failure affecting one target does not stop the remaining targets from being scanned.

For example:

```bash
python myrecon.py example.com invalid-domain.example github.com
```

The valid targets can still complete even if one target fails.

## JSON Reports

After each scan, MyRecon saves the collected results to:

```text
reports/recon_report.json
```

A report contains structured information such as:

```json
{
    "target_count": 1,
    "results": [
        {
            "input_target": "example.com",
            "success": true,
            "url": "https://example.com",
            "status_code": 200,
            "response_time_ms": 145.25,
            "headers": {
                "server": "nginx",
                "content_type": "text/html",
                "content_length": 1256
            },
            "security_headers": {
                "Content-Security-Policy": true,
                "X-Frame-Options": false,
                "X-Content-Type-Options": true,
                "Strict-Transport-Security": true,
                "Referrer-Policy": false
            },
            "redirects": {
                "detected": false,
                "count": 0,
                "final_url": "https://example.com"
            },
            "https": {
                "enabled": true,
                "certificate_cn": "example.com",
                "certificate_expiration": "2026-12-15T23:59:59+00:00"
            }
        }
    ]
}
```

Failed targets are also represented in the report with an error message instead of causing the entire application to terminate.

## Logging

MyRecon logs application activity and errors to:

```text
recon.log
```

Logged events include:

* Scan operations
* Successful scans
* Validation errors
* Connection failures
* HTTP errors
* Unexpected errors
* JSON report creation

## Testing

Run the complete automated test suite with:

```bash
pytest -v
```

Run the test suite with coverage reporting:

```bash
pytest --cov=. --cov-report=term-missing
```

The project test suite covers all main application components, including:

* CLI parsing
* Input validation
* HTTP client behavior
* HTTP request handling
* Response analysis
* Redirect detection
* Security header detection
* HTTPS certificate handling
* JSON report generation
* Logging
* Terminal formatting
* Scanner orchestration
* Concurrent scanning
* Error handling
* Application entry point

## Error Handling

MyRecon is designed so that a failure involving one target does not terminate a multi-target scan.

Handled errors include:

* Invalid targets
* Unsupported URL schemes
* Invalid ports
* Request timeouts
* Connection errors
* General HTTP request errors
* Certificate inspection errors
* Unexpected scanning errors
* JSON report writing errors

## Disclaimer

MyRecon is intended for educational purposes and authorized security testing.

Only scan websites, systems, and infrastructure that you own or have explicit permission to test.

The user is responsible for ensuring that use of this tool complies with all applicable laws, policies, and authorization requirements.
