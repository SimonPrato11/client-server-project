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

if __name__ == "__main__":
    main()
