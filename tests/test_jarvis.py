import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jarvis


class JarvisCoreTests(unittest.TestCase):
    def test_wake_names(self):
        self.assertEqual(jarvis.extract_wake("Mahi open notepad"), "open notepad")
        self.assertEqual(jarvis.extract_wake("Jarvis"), "")
        self.assertIsNone(jarvis.extract_wake("hello assistant"))

    def test_shutdown_names(self):
        self.assertEqual(jarvis.execute("shutdown mahi"), "SHUTDOWN")
        self.assertEqual(jarvis.execute("shutdown jarvis"), "SHUTDOWN")

    def test_memory_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "memory.json"
            jarvis.save(path, {"notes": ["test"]})
            self.assertEqual(jarvis.load(path, {}), {"notes": ["test"]})

    @patch.object(jarvis.psutil, "cpu_percent", return_value=10)
    @patch.object(jarvis.psutil, "virtual_memory")
    def test_system_status(self, mock_memory, _mock_cpu):
        mock_memory.return_value.percent = 20
        self.assertEqual(jarvis.execute("system status"), "CPU 10 percent, RAM 20 percent.")


if __name__ == "__main__":
    unittest.main()
