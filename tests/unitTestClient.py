# --------------------------------------------------------------------------------
# Unit Tests for Client Module
# --------------------------------------------------------------------------------
# Author: Luca Simeone
# Date: 7th May, 2024
# Description:
#     This script provides unit tests for the client module, which handles data
#     serialization and network communication with a server. The tests cover
#     serialization in binary, JSON, and XML formats and ensure that the client's
#     main function appropriately manages socket connections and sends data as
#     expected.
#
#     These tests aim to verify that the client module correctly serializes data
#     into the specified format and handles socket communication effectively,
#     using mocks for socket methods to ensure that no actual network communication
#     is performed during the tests.
#
# Usage:
#     Run this script directly to execute all unit tests for the client module.
#     Ensure that the client module and its dependencies are correctly configured
#     in your environment.
# --------------------------------------------------------------------------------

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
import xml.etree.ElementTree as ET
import pickle

# Append the path to the src directory so that Python can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import client  # Import module


class TestClient(unittest.TestCase):
    def test_serialize_data_binary(self):
        """Test serialization of data into binary format."""
        data = {"name": "John", "age": 30, "city": "New York"}
        serialized_data = client.serialize_data(data, "binary")
        deserialized_data = pickle.loads(serialized_data)
        self.assertEqual(deserialized_data, data)

    def test_serialize_data_json(self):
        """Test serialization of data into JSON format."""
        data = {"name": "John", "age": 30, "city": "New York"}
        serialized_data = client.serialize_data(data, "json")
        deserialized_data = json.loads(serialized_data.decode())
        self.assertEqual(deserialized_data, data)

    def test_serialize_data_xml(self):
        """Test serialization of data into XML format."""
        data = {"name": "John", "age": 30, "city": "New York"}
        serialized_data = client.serialize_data(data, "xml")
        root = ET.fromstring(serialized_data)
        deserialized_data = {
            child.tag: int(child.text) if child.tag == "age" else child.text
            for child in root
        }
        self.assertEqual(deserialized_data, data)

    @patch("socket.socket")
    def test_main(self, mock_socket_class):
        """Test the main function for proper socket usage."""
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        mock_socket_instance.connect.return_value = (
            None  # Explicitly return None for clarity
        )

        # Call the main function
        client.main()

        # Verify that connect was called
        mock_socket_instance.connect.assert_called_with(("localhost", 12345))
        # Add any additional behavior checks such as sendall calls etc.


if __name__ == "__main__":
    unittest.main()
