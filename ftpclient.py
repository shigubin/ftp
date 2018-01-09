import os
import socket
import json

HOST = "localhost"
PORT = 8888

class FtpClient:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

    def login(self, cmd_list):
        cmd_dict = {"action":cmd_list[0], "username":cmd_list[1], "password":cmd_list[2]}
        self.sock.sendall(json.dumps(cmd_dict).encode("utf-8"))

    def run(self):
        while True:
            cmd_line = input(">>>:").strip()
            cmd_list = cmd_line.split()

            if hasattr(self, cmd_list[0]):
                func = getattr(self, cmd_list[0])
                func(cmd_list)

            data = self.sock.recv(1024)
            print(data.decode())

if __name__ == "__main__":
    ftpClient = FtpClient()
    ftpClient.run()