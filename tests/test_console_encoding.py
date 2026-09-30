import sys
import unittest
from unittest.mock import patch

from mapgen.console import configure_utf8_stdio


class ConsoleEncodingTest(unittest.TestCase):
    def test_reconfigures_stdout_and_stderr_as_utf8(self):
        stdout = _FakeStream()
        stderr = _FakeStream()

        with patch.object(sys, "stdout", stdout), patch.object(sys, "stderr", stderr):
            configure_utf8_stdio()

        self.assertEqual(stdout.options, {"encoding": "utf-8", "errors": "replace"})
        self.assertEqual(stderr.options, {"encoding": "utf-8", "errors": "replace"})


class _FakeStream:
    def __init__(self):
        self.options = None

    def reconfigure(self, **options):
        self.options = options


if __name__ == "__main__":
    unittest.main()
