"""
PII-Safe Logger Package

A logging system that enforces consent checks and redacts sensitive data.
"""

from .logger import BeaconLogger, AuditLevel

__all__ = ["BeaconLogger", "AuditLevel"]
