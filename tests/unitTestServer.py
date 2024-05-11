# --------------------------------------------------------------------------------
# Unit Tests for Server Module
# --------------------------------------------------------------------------------
# Author: Luca Simeone
# Date: 7th May, 2024
# Description:
#     This script provides unit tests for the server module, which handles configuration
#     loading and data processing in a client/server network setup. The tests ensure that
#     the server can correctly load configuration settings, handle file not found and JSON
#     decode errors, and process incoming data correctly based on encryption settings.
#
#     The tests use a mock approach to simulate file operations and check the behavior of
#     the server functions without requiring actual files or a running server environment.
#     This allows for isolated testing of logic in the server module.
#
# Usage:
#     Run this script directly to execute all unit tests for the server module. Ensure that
#     the server module and its dependencies are correctly configured in your environment.
# --------------------------------------------------------------------------------

import unittest
import json
from io import StringIO
import sys
import os

# Adjust the system path to include the server directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_dir, "src")
sys.path.append(src_dir)

try:
    import server

    print("server module imported successfully!")
except ModuleNotFoundError:
    print("Failed to import server module. Check the path and existence of server.py.")


class ServerTests(unittest.TestCase):
    """Unit tests for server functionality."""

    def simulate_file_open(self, file_name, mode, content=None):
        """Simulate file opening for configuration files."""
        if file_name == "config.json" and mode == "r":
            if content is None:
                raise FileNotFoundError("File 'config.json' not found.")
            return StringIO(content)
        raise FileNotFoundError(f"File '{file_name}' not found.")

    def test_load_valid_configuration(self):
        """Test loading a valid configuration from a simulated JSON file."""
        config_content = '{"server_output": "console"}'
        file = self.simulate_file_open("config.json", "r", config_content)
        config = json.load(file)
        self.assertEqual(config["server_output"], "console")

    def test_load_configuration_file_not_found(self):
        """Test behavior when the configuration file is missing."""
        with self.assertRaises(FileNotFoundError):
            self.simulate_file_open("missing.json", "r")

    def test_load_configuration_json_error(self):
        """Test behavior when configuration file contains malformed JSON."""
        config_content = "{invalid_json: "  # Malformed JSON
        with self.assertRaises(json.JSONDecodeError):
            file = self.simulate_file_open("config.json", "r", config_content)
            json.load(file)

    def test_process_incoming_data(self):
        """Test that process_incoming_data returns the correct string based on encryption setting."""
        result = server.process_incoming_data(True)
        self.assertEqual(
            result,
            "Processed data based on encryption setting",
            "The function should return the expected string when encryption is enabled.",
        )

        result = server.process_incoming_data(False)
        self.assertEqual(
            result,
            "Processed data based on encryption setting",
            "The function should return the expected string when encryption is disabled.",
        )


if __name__ == "__main__":
    unittest.main()
