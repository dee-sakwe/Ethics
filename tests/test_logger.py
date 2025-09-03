import unittest
from io import StringIO
import sys
import os

# Add the parent directory to the path so we can import beacon_logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beacon_logger.logger import BeaconLogger, AuditLevel


class TestBeaconLogger(unittest.TestCase):
    def setUp(self):
        self.held_stdout = sys.stdout
        sys.stdout = self.log_capture = StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout

    def test_pii_redaction(self):
        logger = BeaconLogger()
        message = "User contact: test@example.com, phone: 555-123-4567. Last seen at 40.7128, -74.0060."
        logger.log(message, user_id="user_has_consent")
        output = self.log_capture.getvalue()
        self.assertIn("[REDACTED_EMAIL]", output)
        self.assertIn("[REDACTED_PHONE]", output)
        self.assertIn("[REDACTED_GPS]", output)
        self.assertNotIn("test@example.com", output)

    def test_consent_denied(self):
        logger = BeaconLogger()
        sensitive_message = "This user's secret is password123"
        logger.log(sensitive_message, user_id="user_no_consent")
        output = self.log_capture.getvalue()
        self.assertIn("CONSENT_FAILURE", output)
        self.assertNotIn(
            "password123", output
        )  # Critical: original message must not be logged

    def test_audit_level(self):
        logger = BeaconLogger(level=AuditLevel.MINIMAL)

        # This should log
        logger.log(
            "Minimal log message.", user_id="user_has_consent", level=AuditLevel.MINIMAL
        )
        # This should NOT log
        logger.log(
            "Diagnostic log message.", user_id="user_has_consent", level=AuditLevel.DIAG
        )

        output = self.log_capture.getvalue()
        self.assertIn("Minimal log message.", output)
        self.assertNotIn("Diagnostic log message.", output)

    def test_no_pii_message(self):
        logger = BeaconLogger()
        message = "User performed a search action."
        logger.log(message, user_id="user_has_consent")
        output = self.log_capture.getvalue()
        self.assertIn(message, output)
        self.assertNotIn("[REDACTED", output)


if __name__ == "__main__":
    unittest.main()
