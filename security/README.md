# Security Module

The `security` package contains the security-related analysis functionality used by MyRecon.

It checks common HTTP security headers and retrieves basic HTTPS certificate information.

## Files

### `headers.py`

Checks whether the following HTTP security headers are present:

- `Content-Security-Policy`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Strict-Transport-Security`
- `Referrer-Policy`

The result is returned as a dictionary of Boolean values.

Example:

```python
{
    "Content-Security-Policy": True,
    "X-Frame-Options": False,
    "X-Content-Type-Options": True,
    "Strict-Transport-Security": True,
    "Referrer-Policy": False,
}
```

MyRecon currently checks whether each header is present.

It does not analyze whether the individual header configuration is secure.

### `certificate.py`

Handles HTTPS and SSL/TLS certificate inspection.

For HTTPS targets, it attempts to retrieve:

- Whether HTTPS is enabled
- Certificate Common Name (CN)
- Certificate expiration date

The module uses Python's:

- `ssl`
- `socket`
- `urllib.parse`

Certificate inspection failures are handled gracefully and do not stop the main website scan.

## Flow

```text
HTTP Response
    ↓
headers.py
    ↓
Security Header Results

Final URL
    ↓
certificate.py
    ↓
HTTPS Certificate Information
```
