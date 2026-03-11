import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 9999))
    s.listen()
    print("Listening on port 9999...")
    conn, addr = s.accept()  # blocks, waiting for a connection