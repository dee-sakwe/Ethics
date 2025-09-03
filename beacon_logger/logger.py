import re
from enum import Enum
from datetime import datetime, timezone
from . import consent_manager


class AuditLevel(Enum):
    NONE = 0
    MINIMAL = 1  # Default
    DIAG = 2  # Diagnostic


class BeaconLogger:
    """A PII-safe logger that enforces consent checks and redacts sensitive data."""

    def __init__(self, level: AuditLevel = AuditLevel.MINIMAL):
        self.level = level
        self.pii_patterns = {
            "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "PHONE": re.compile(r"\(?\b\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
            "GPS": re.compile(
                r"\b[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)\b"
            ),
        }

    def _redact(self, message: str) -> str:
        """Finds and redacts all known PII patterns in a message."""
        redacted_message = message
        for pii_type, pattern in self.pii_patterns.items():
            redacted_message = pattern.sub(f"[REDACTED_{pii_type}]", redacted_message)
        return redacted_message

    def log(self, message: str, user_id: str, level: AuditLevel = AuditLevel.MINIMAL):
        """
        Logs a message if the level is sufficient, consent is given, and PII is redacted.
        """
        # 1. Enforce audit level
        if level.value > self.level.value:
            return  # Don't log if message level is higher than logger's configured level

        # 2. Enforce consent
        try:
            consent_manager.require_consent(user_id)
        except consent_manager.ConsentError as e:
            # Log a consent failure without logging the original sensitive message
            ts = datetime.now(timezone.utc).isoformat()
            print(f"[{ts}] [LEVEL: MINIMAL] [USER: {user_id}] CONSENT_FAILURE: {e}")
            return

        # 3. Redact PII
        redacted_message = self._redact(message)

        # 4. Write log
        ts = datetime.now(timezone.utc).isoformat()
        print(f"[{ts}] [LEVEL: {level.name}] [USER: {user_id}] {redacted_message}")
