# Test Suite

The `tests` directory contains the automated test suite for MyRecon.

Tests are written using `pytest`.

Mocking is used where appropriate so unit tests do not depend on external websites, network availability, SSL connections, or filesystem permissions.

## Test Files

### `test_parser.py`

Tests:

- Single target parsing
- Multiple target parsing
- Full URL parsing
- Missing required targets

### `test_validator.py`

Tests:

- Domain normalization
- HTTP URLs
- HTTPS URLs
- Subdomains
- IP addresses
- `localhost`
- Empty targets
- Whitespace
- Unsupported schemes
- Invalid domains
- Invalid ports
- Excessively long hostnames
- Missing hostnames

### `test_client.py`

Tests:

- HTTP client initialization
- Default timeout
- Custom timeout
- User-Agent configuration
- GET requests
- Redirect configuration
- Session cleanup

### `test_request.py`

Tests:

- Successful GET requests
- Response time measurement
- Default timeout
- Client cleanup after successful requests
- Client cleanup after failed requests

### `test_response.py`

Tests:

- Status code extraction
- Response time
- HTTP headers
- Missing headers
- Numeric Content-Length values
- Invalid Content-Length values
- Redirect detection
- Redirect count
- Final destination URL

### `test_headers.py`

Tests:

- All security headers present
- All security headers missing
- Individual security headers
- Unrelated HTTP headers

### `test_certificate.py`

Tests:

- Certificate Common Name extraction
- Missing Common Name
- Certificate expiration dates
- Missing expiration dates
- HTTP targets
- HTTPS targets
- Missing hostnames
- Default HTTPS port
- Custom HTTPS ports
- Certificate connection errors

### `test_json_report.py`

Tests:

- JSON report creation
- Correct report contents
- Multiple reports
- Empty report lists
- Automatic directory creation
- Filesystem errors

### `test_logger.py`

Tests:

- Custom log files
- Default `recon.log`
- Log message output

### `test_formatter.py`

Tests:

- Successful terminal output
- Failed scans
- Missing values
- Redirect information
- Security headers
- HTTPS enabled
- HTTPS disabled
- Missing certificate information
- JSON report locations
- JSON save errors

### `test_scanner.py`

Tests:

- Successful target scanning
- Validation failures
- Request timeouts
- Connection errors
- General request errors
- Unexpected exceptions
- Empty target lists
- Single-target scanning
- Concurrent multi-target scanning

### `test_myrecon.py`

Tests:

- Main application execution
- Single and multiple report output
- JSON report saving
- JSON save errors
- Script entry-point execution

## Running Tests

Run all tests:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

The current test suite contains 77 passing tests and achieves 100% measured statement coverage across the project.

## Testing Philosophy

The test suite aims to keep tests:

- Isolated
- Repeatable
- Fast
- Independent of external network availability

Network operations, HTTP sessions, SSL connections, and error conditions are mocked where appropriate.

Manual integration tests are still useful for verifying real-world behavior against live websites.
