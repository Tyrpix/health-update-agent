import unittest
import main
from datetime import datetime


class TestMain(unittest.TestCase):

    def test_payload(self):
        now = datetime.now()
        expected_result = {
            "service": "test",
            "date": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "environment": "testing",
            "eventType": "deployment",
            "message": "Deployed Version: v.1.0"

        }
        result = main.payload("test", "v.1.0", "testing")
        self.assertTrue(result, expected_result)