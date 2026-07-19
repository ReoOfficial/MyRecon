# CLI Module

The `cli` package handles command-line input and target validation for MyRecon.

Its responsibility is to process the targets provided by the user before the scanning process begins.

## Files

### `parser.py`

Handles command-line argument parsing using Python's `argparse` module.

It allows the user to provide one or more targets.

Example:

```bash
python myrecon.py example.com
```

Multiple targets are also supported:

```bash
python myrecon.py google.com github.com openai.com
```

The parsed targets are stored in:

```python
args.targets
```

### `validator.py`

Handles target normalization and validation.

It accepts domains and full HTTP or HTTPS URLs.

For example:

```text
example.com
```

is normalized to:

```text
https://example.com
```

The validator checks:

- Empty input
- Whitespace
- Supported HTTP and HTTPS schemes
- Valid hostnames
- Domain structure
- IP addresses
- `localhost`
- Port validity

Invalid targets raise a `ValueError` and are handled safely by the scanner.

## Flow

```text
User Input
    ↓
parser.py
    ↓
validator.py
    ↓
Validated URL
    ↓
Scanner
```
