# --------------------------------------------------------------------------------
# Simple Server for Client/Server Communication
# --------------------------------------------------------------------------------
# Author: Luca Simeone
# Date: 6th May, 2024
# Description:
#     This script implements a simple server using the socket module to accept incoming
#     connections and handle data according to specified configurations. It can process
#     data in different formats (e.g., plain text, JSON) and handle encrypted data.
#     The server reads configuration from a JSON file, which includes settings like
#     whether to encrypt text data and whether to output to the console or a file.
#
#     The server listens on all network interfaces on a specified port and handles
#     incoming data based on the configurations specified in 'config.json'. If the
#     data includes encrypted text, it uses functions from an external cryptography
#     helper module to decrypt the text before processing.
#
# Usage:
#     To run the server, ensure that the 'config.json' file is in the same directory
#     as this script or adjust the path accordingly. Run this script directly from the
#     command line. The server will start listening for incoming connections and process
#     data as clients connect and send information.
# --------------------------------------------------------------------------------

import socket
import json
import sys
import os

# Ensure that Python can find and load other modules from the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from cryptographyHelper import decrypt_message


def load_configuration(file_path):
    """
    Load a configuration from a JSON file.

    This function attempts to open and read a JSON file, returning the parsed
    content. It handles file-not-found and JSON decoding errors by printing an error
    message and returning None.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        dict or None: The parsed JSON data as a dictionary if the file is successfully read and parsed.
                      Returns None if the file does not exist or an error occurs during JSON decoding.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Missing 'config.json' file.")
        return None
    except json.JSONDecodeError:
        print("Error decoding 'config.json'. Check its format.")
        return None


def process_incoming_data(encrypt):
    """Simple logic to simulate data processing depending on the encryption setting."""
    return "Processed data based on encryption setting"


def main():
    """Main function to set up and run the server."""
    host = ""  # Bind to all interfaces
    port = 12345

    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Server is listening for incoming connections...")
    except socket.error as e:
        print(f"Failed to bind or listen on port {port}: {e}")
        sys.exit(1)

    try:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        config = load_configuration("config.json")
        if config is None:
            conn.close()
            return

        received_dict = conn.recv(1024)
        print("Received dictionary:", received_dict.decode())

        received_text = conn.recv(1024)
        if config.get("encrypt_text_file"):
            key, encrypted_text = received_text.split(b"|||", 1)
            decrypted_text = decrypt_message(encrypted_text, key)
            print("Received encrypted text:", decrypted_text)
        else:
            print("Received text:", received_text.decode())

        if config.get("server_output") == "file":
            with open(config["server_output_file"], "w", encoding="utf-8") as file:
                file.write(
                    str(received_dict.decode()) + "\n" + str(received_text.decode())
                )
    except socket.error as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")
    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    main()
