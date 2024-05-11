# --------------------------------------------------------------------------------
# Client Program for Data Serialization and Sending
# --------------------------------------------------------------------------------
# Author: Luca Simeone
# Date: 6th May, 2024
# Description:
#     This module defines functionality for a client in a client-server architecture,
#     which serializes data in various formats (binary, JSON, XML) and sends it over
#     a network. It handles configuration loading, data serialization according to
#     user preferences, and encrypted text transmission.
#
#     The program supports sending a dictionary serialized in the user's chosen format
#     and optionally sending text data encrypted. The client establishes a connection
#     with the server, sends the serialized and optionally encrypted data, then closes
#     the connection.
#
# Usage:
#     Run this script directly to connect to a server specified by the host and port
#     in the script. Ensure the server is running before starting the client. The
#     script reads configuration details from 'config.json', which should include
#     settings for data format and encryption preferences.
# --------------------------------------------------------------------------------

import socket
import json
import pickle
import xml.etree.ElementTree as ET
import sys
import os

# Ensure the Python environment recognizes the src directory for module imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cryptographyHelper import encrypt_message, generate_key


def load_configuration(config_path):
    """Load and return the configuration from a JSON file."""
    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: The configuration file '{config_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The configuration file '{config_path}' contains invalid JSON.")
        sys.exit(1)


def serialize_data(data, format_type):
    """Serialize data into the specified format (binary, JSON, XML)."""
    if format_type == "binary":
        return pickle.dumps(data)
    elif format_type == "json":
        return json.dumps(data).encode()
    elif format_type == "xml":
        root = ET.Element("dictionary")
        for key, val in data.items():
            ET.SubElement(root, key).text = str(val)
        return ET.tostring(root)


def main():
    """Main function to connect to the server and handle data serialization and sending."""
    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "config.json"
    )
    config = load_configuration(config_path)

    host = "localhost"
    port = 12345
    client_socket = socket.socket()

    try:
        client_socket.connect((host, port))
        print("Connected to server.")

        # Dictionary data serialization and sending
        sample_dict = {"name": "John", "age": 30, "city": "New York"}
        serialized_dict = serialize_data(sample_dict, config["dictionary_format"])
        client_socket.sendall(serialized_dict)

        # Text file data handling and sending
        text_data = "Hello, this is a sample text file content."
        if config["encrypt_text_file"]:
            key = generate_key()
            encrypted_text = encrypt_message(text_data, key)
            client_socket.sendall(key + b"|||" + encrypted_text)
        else:
            client_socket.sendall(text_data.encode())

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
