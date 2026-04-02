import socket

def banner_server(host='127.0.0.1', port=9999, banner=b'MyService v1.0 ready\r\n'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                conn.sendall(banner)

banner_server()