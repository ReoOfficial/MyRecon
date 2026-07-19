# Core Module

The `core` package contains the main scanning and HTTP functionality of MyRecon.

It coordinates HTTP requests, analyzes responses, and manages single-target and concurrent multi-target scans.

## Files

### `client.py`

Provides the `HttpClient` class.

The HTTP client is responsible for:

- Creating a reusable `requests.Session`
- Configuring the MyRecon User-Agent
- Applying request timeouts
- Following HTTP redirects
- Closing the HTTP session

### `request.py`

Handles GET request execution.

It:

- Creates an `HttpClient`
- Sends the HTTP GET request
- Measures total request time
- Converts the response time to milliseconds
- Ensures the HTTP client is closed after the request

### `response.py`

Analyzes HTTP responses and extracts:

- Status code
- Response time
- Server header
- Content-Type
- Content-Length
- Redirect detection
- Redirect count
- Final destination URL

Missing optional response headers are handled safely.

### `scanner.py`

Acts as the central controller for scanning targets.

For each target, it coordinates:

```text
Validation
    ↓
HTTP Request
    ↓
Response Analysis
    ↓
Security Header Check
    ↓
HTTPS Certificate Check
    ↓
Structured Report
```

It also handles:

- Validation errors
- Request timeouts
- Connection errors
- General HTTP request errors
- Unexpected exceptions

When multiple targets are provided, `ThreadPoolExecutor` is used to scan them concurrently.

A failure affecting one target does not stop the remaining targets from being scanned.

## Flow

```text
scan_targets()
    ↓
ThreadPoolExecutor
    ↓
scan_target()
    ↓
Validator
    ↓
HTTP Request
    ↓
Response Analysis
    ↓
Security Analysis
    ↓
Report Dictionary
```
