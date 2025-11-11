import socket
import struct
import argparse
import logging

def setup_logging(log_location):
    logging.basicConfig(filename=log_location, level=logging.INFO, format='%(message)s')

def log(msg):
    logging.info(msg)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-l", "--log", required=True)
    return parser.parse_args()

def handle_client(conn, addr):
    log(f"Received connection from (IP, PORT): {addr}")

    # ----- Receive hello header -----
    header = conn.recv(12)
    if len(header) < 12:
        return

    version, mtype, msglen = struct.unpack(">III", header)
    log(f"Received Data: version: {version} message_type: {mtype} length: {msglen}")
    message = conn.recv(msglen).decode()

    # Version check
    if version != 17:
        log("VERSION MISMATCH")
        conn.sendall(b"VERSION MISMATCH")
        return
    else:
        log("VERSION ACCEPTED")

    # Hello Handling
    if message.upper() == "HELLO":
        log("Received Message Hello")
        conn.sendall(b"HELLO")

        # ----- Receive command header -----
        cmd_header = conn.recv(12)
        if len(cmd_header) < 12:
            return

        version2, mtype2, cmdlen = struct.unpack(">III", cmd_header)
        cmd_message = conn.recv(cmdlen).decode()
        log(f"Received Data: version: {version2} message_type: {mtype2} length: {cmdlen}")

        # Command Handling
        if version2 != 17:
            log("VERSION MISMATCH")
            conn.sendall(b"VERSION MISMATCH")
            return
        else:
            log("VERSION ACCEPTED")

        if mtype2 == 1 and cmd_message.upper() == "LIGHTON":
            log("EXECUTING SUPPORTED COMMAND: LIGHTON")
            # Simulate LED ON
        elif mtype2 == 2 and cmd_message.upper() == "LIGHTOFF":
            log("EXECUTING SUPPORTED COMMAND: LIGHTOFF")
            # Simulate LED OFF
        else:
            log(f"IGNORING UNKNOWN COMMAND: {cmd_message}")

        conn.sendall(b"SUCCESS")
        log("Returning SUCCESS")

def main():
    args = parse_args()
    setup_logging(args.log)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", args.port))
    server_socket.listen()
    log(f"Listening on port {args.port}")

    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)
        conn.close()

if __name__ == "__main__":
    main()
