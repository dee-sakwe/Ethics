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