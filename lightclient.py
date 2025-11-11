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
    parser.add_argument("-s", "--server", required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-l", "--log", required=True)
    return parser.parse_args()

def send_packet(conn, version, mtype, message):
    msg_bytes = message.encode()
    header = struct.pack(">III", version, mtype, len(msg_bytes))
    conn.sendall(header)
    conn.sendall(msg_bytes)

def recv_packet(conn):
    header = conn.recv(12)
    if len(header) < 12:
        return None, None, None
    version, mtype, msglen = struct.unpack(">III", header)
    if msglen == 0:
        return version, mtype, ""
    message = conn.recv(msglen).decode()
    return version, mtype, message

def main():
    args = parse_args()
    setup_logging(args.log)
    log("Connecting to server...")

    conn = socket.create_connection((args.server, args.port))

    # Send hello
    log("Sending HELLO Packet")
    send_packet(conn, 17, 0, "HELLO")

    # Receive hello reply
    reply = conn.recv(64)
    if reply == b"VERSION MISMATCH":
        log("VERSION MISMATCH")
        conn.close()
        return
    elif reply == b"HELLO":
        log("VERSION ACCEPTED")
        log("Received Message Hello")

    # Send command (change to LIGHTON or LIGHTOFF as needed)
    cmd = "LIGHTON"
    log("Sending command")
    send_packet(conn, 17, 1, cmd)

    # Receive server reply
    reply = conn.recv(64)
    if reply == b"SUCCESS":
        log("Received Message SUCCESS")
        log("Command Successful")
    else:
        log("Received Message " + reply.decode())

    log("Closing socket")
    conn.close()

if __name__ == "__main__":
    main()
