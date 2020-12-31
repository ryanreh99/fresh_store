import os
import json
import unittest
from unittest.mock import patch

import fresh_store
from fresh_store.exceptions import *

test_data_store_file_name: str = "TEST_DATA_STORE.json"
test_file: str = os.path.join(os.getcwd(), test_data_store_file_name)
test_json_1: str = os.path.join(os.getcwd(), "tests/examples/example_1.json")
test_json_2: str = os.path.join(os.getcwd(), "tests/examples/example_2.json")


@patch('fresh_store.data.DATA_STORE_FILE_NAME', "TEST_DATA_STORE.json")
class TestFreshStore(unittest.TestCase):
    def setUp(self):
        self.fresh_obj = fresh_store.FreshStore(test_file)

    @patch('fresh_store.data.MAX_KEY_CAPACITY', 5)
    @patch('fresh_store.data.MAX_VALUE_SIZE', 15)
    @patch('fresh_store.data.MAX_DATA_STORE_SIZE', 15)
    def test_validation(self):
        # key
        with self.assertRaises(KeyCapacityExceededError):
            self.fresh_obj.create("a bad key", test_json_1)

        # value
        with self.assertRaises(ValueCapacityExceededError):
            self.fresh_obj.create("abc", test_json_2)

        # data store
        with self.assertRaises(ValueCapacityExceededError):
            self.fresh_obj.create("abc", test_json_1)

    def test_api(self):
        # CREATE
        self.fresh_obj.create("abc", test_json_1)
        self.fresh_obj.create("def", test_json_2, 0)

        with self.assertRaises(KeyAlreadyExists):
            self.fresh_obj.create("abc", test_json_2)

        # READ
        ret = self.fresh_obj.read("abc")
        expected_json = json.dumps(ret, sort_keys=True)

        with open(test_json_1, "r") as f:
            file_data = f.read()
        actual_json = json.dumps(json.loads(file_data), sort_keys=True)

        self.assertEqual(actual_json, expected_json)

        # TTL
        with self.assertRaises(KeyExpired):
            self.fresh_obj.read("def")
            self.fresh_obj.delete("def")

        # DELETE
        ret = self.fresh_obj.delete("abc")
        expected_json = json.dumps(ret, sort_keys=True)
        self.assertEqual(actual_json, expected_json)

        ret = self.fresh_obj.read("abc")
        self.assertTrue(ret == "")

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(test_file))


if __name__ == '__main__':
    unittest.main()
