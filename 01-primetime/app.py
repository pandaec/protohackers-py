import argparse
import asyncio
import socket
import json
from math import floor, sqrt

host = "0.0.0.0"
bufsize = 2048


async def is_prime(n):
    return is_prime_sync(n)


def is_prime_sync(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, floor(sqrt(n)), 2):
        if n % i == 0:
            return False
    return True


async def handle_client(client):
    loop = asyncio.get_event_loop()
    data = ""
    while True:
        data += (await loop.sock_recv(client, bufsize)).decode()
        if data == "":
            break

        lines = [x for x in data.split("\n") if x]
        if lines[-1:][-1:] != "\n":
            data = data[-1:]
            lines = lines[:-1]

        for line in lines:
            o = json.loads(line)
            print(o)
            method = o.get("isMethod")
            number = o.get("number")
            if method != "isPrime" or type(number) != "number":
                # malform request
                await loop.sock_sendall(client, line.encode())

            res = {"method": "isPrime"}
            res["prime"] = await is_prime(number)

            response = json.dumps(res)
            print(response)
            await loop.sock_sendall(client, response.encode())
    client.close()


async def run_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (host, port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(server_address)
        s.listen(8)
        s.setblocking(False)
        print("Starting server on %s port %s" % server_address)

        loop = asyncio.get_event_loop()

        while True:
            client, addr = await loop.sock_accept(s)
            loop.create_task(handle_client(client))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server")
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    asyncio.run(run_server(port))
