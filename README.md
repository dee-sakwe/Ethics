# Beacon-Grade PII-Safe Logging Utility

## Overview
This module provides a `BeaconLogger` class designed for use in production systems at Meta. It ensures that logs are scrubbed of Personally Identifiable Information (PII) before being written and that logging respects user consent choices. It is a foundational tool for building trustworthy features.

## Features
- **PII Redaction:** Automatically detects and redacts emails, phone numbers, and GPS coordinates from log messages using regular expressions.
- **Consent-Aware Logging:** Integrates with a consent manager to ensure logs for a specific user are only written if that user has provided consent. It fails safely by logging a consent failure notice without exposing the original message.
- **Configurable Audit Levels:** Supports `NONE`, `MINIMAL`, and `DIAG` levels to control logging verbosity in different environments. Defaults to `MINIMAL` for safety.

## Setup and Running Tests
This module has no external dependencies.
To run the unit tests, navigate to the root directory and run:
```bash
python -m unittest tests.test_logger
```

### Known Limitations
1. Regex is Not Foolproof: The regex-based detection can be circumvented by creatively formatted PII (e.g., test (at) example.com). It is a strong mitigation but not a perfect guarantee.

2. No Name Detection: Detecting personal names is a complex Natural Language Processing task (Named Entity Recognition) with a high risk of false positives (e.g., redacting the word "Mark" in "bookmark"). This feature was omitted to avoid corrupting logs.

3. Mock Consent Manager: The provided consent_manager is a simple mock. In production, it must be replaced with a client for the actual, highly-available consent service.

### Future Work
- Integrate NER Model: For services that require it, integrate a lightweight Named Entity Recognition (NER) model to detect and redact a wider class of PII, like names and addresses.

- Structured Logging: Output logs as JSON objects. This makes them machine-readable and allows for fields like user_id and pii_redacted_count to be queried systematically.

- CI/CD Integration: Create a linter that flags direct calls to print() or the standard logging library in our codebase, forcing the use of BeaconLogger to ensure compliance.

