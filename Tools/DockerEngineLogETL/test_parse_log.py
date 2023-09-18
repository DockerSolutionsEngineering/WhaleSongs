#!/usr/bin/env python3
import unittest
from parse_log import (
    parse_container_start_or_restart_log,
    parse_container_stop_log,
    parse_image_create_log,
    parse_container_delete_log,
    parse_image_delete_log
)
from sample_data import sample_data


class TestLogParsing(unittest.TestCase):

    def setUp(self):
        self.sample_data = sample_data


    def test_parse_container_start_or_restart_log(self):
        for log_line in self.sample_data["start_or_restart"]:
            datetime, name, operation, details, duration = parse_container_start_or_restart_log(log_line)
            self.assertIsNotNone(datetime)
            self.assertIsNotNone(name)
            self.assertIsNotNone(operation)
            self.assertIsNotNone(duration)


    def test_parse_container_stop_log(self):
        for log_line in self.sample_data["stop"]:
            datetime, name, operation, details, duration = parse_container_stop_log(log_line)
            self.assertIsNotNone(datetime)
            self.assertIsNotNone(name)
            self.assertIsNotNone(operation)
            self.assertIsNotNone(duration)


    def test_parse_image_create_log(self):
        for log_line in self.sample_data["image_create"]:
            datetime, name, operation, details, duration = parse_image_create_log(log_line)
            self.assertIsNotNone(datetime)
            self.assertIsNotNone(name)
            self.assertIsNotNone(operation)
            self.assertIsNotNone(duration)


    def test_parse_container_delete_log(self):
        for log_line in self.sample_data["container_delete"]:
            datetime, name, operation, details, duration = parse_container_delete_log(log_line)
            self.assertIsNotNone(datetime)
            self.assertIsNotNone(name)
            self.assertIsNotNone(operation)
            self.assertIsNotNone(duration)


    def test_parse_image_delete_log(self):
        for log_line in self.sample_data["image_delete"]:
            datetime, name, operation, details, duration = parse_image_delete_log(log_line)
            self.assertIsNotNone(datetime)
            self.assertIsNotNone(name)
            self.assertIsNotNone(operation)
            self.assertIsNotNone(duration)


if __name__ == "__main__":
    unittest.main()
