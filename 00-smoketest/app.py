import socket
import argparse

host = "0.0.0.0"
bufsize = 20000
backlog = 10

def echo_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (host, port)
        print("Starting server on %s port %s" % server_address)
        s.bind(server_address)
        s.listen(backlog)

        while True:
            client, addr = s.accept()
            data = client.recv(bufsize, socket.MSG_WAITALL)
            client.send(data)
            print(data)
            client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server")
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
