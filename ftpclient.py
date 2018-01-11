import os
import socket
import json


HOST = "localhost"
PORT = 8888

class FtpClient:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))
        self.prompt = ">>>:"

    def login(self, cmd_list):
        self.username = cmd_list[1]
        cmd_dict = {"action":cmd_list[0], "username":cmd_list[1], "password":cmd_list[2]}
        self.sock.sendall(json.dumps(cmd_dict).encode("utf-8"))

        data = self.sock.recv(1024)
        msg_dict = json.loads(data.decode())
        if msg_dict["ret"] == True:
            self.prompt = self.username + '@ftpserver-' + msg_dict["cur_dir"] + ':'
        else:
            print("sorry! auth failed")

    def show(self, cmd_list):
        cmd_dict = {"action": cmd_list[0]}
        self.sock.sendall(json.dumps(cmd_dict).encode("utf-8"))

        data = self.sock.recv(1024)
        data = data.decode()
        print(self.prompt + data)

    def cd(self, cmd_list):
        cmd_dict = {"action":cmd_list[0], "dir":cmd_list[1]}
        self.sock.sendall(json.dumps(cmd_dict).encode("utf-8")) 

        data = self.sock.recv(1024)
        msg_dict = json.loads(data.decode())

        if msg_dict["ret"] == True:
            self.prompt = self.username + '@ftpserver-' + msg_dict["cur_dir"] + ':'
        else:
            print(self.prompt+"change dirtory failed!")

    def makedir(self, cmd_list):
        cmd_dict = {"action":cmd_list[0], "dir":cmd_list[1]}
        self.sock.sendall(json.dumps(cmd_dict).encode("utf-8"))

        data = self.sock.recv(1024)
        msg = data.decode()

        print(self.prompt + msg)

    def run(self):
        while True:
            cmd_line = input(self.prompt).strip()
            if not cmd_line:
                continue

            cmd_list = cmd_line.split()

            if hasattr(self, cmd_list[0]):
                func = getattr(self, cmd_list[0])
                func(cmd_list)


if __name__ == "__main__":
    ftpClient = FtpClient()
    ftpClient.run()