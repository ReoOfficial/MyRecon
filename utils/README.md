# Utilities Module

The `utils` package contains shared functionality used for terminal output and application logging.

## Files

### `formatter.py`

Handles terminal presentation.

It displays:

- Target information
- HTTP status codes
- Response times
- HTTP headers
- Redirect information
- Security header results
- HTTPS information
- Certificate information
- Errors
- JSON report locations

The module uses `colorama` to provide colored terminal output.

Successful and present values are displayed in green, while missing headers and errors are displayed in red.

Formatting is kept separate from scanning logic so that the core scanning modules remain focused on data collection.

### `logger.py`

Configures Python's logging system.

By default, MyRecon writes logs to:

```text
recon.log
```

Logged events can include:

- Scan starts
- Successful scans
- Concurrent scan operations
- Validation failures
- Connection failures
- HTTP errors
- Unexpected errors
- JSON report creation

The log format includes:

- Timestamp
- Log level
- Module name
- Message

## Flow

```text
Application Events
    ↓
logger.py
    ↓
recon.log

Scan Report
    ↓
formatter.py
    ↓
Colored Terminal Output
```
