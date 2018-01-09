import os
import socketserver
import json
import configparser


class FtpServer(socketserver.BaseRequestHandler):

    def auth(self, username, password):
        config = configparser.ConfigParser()
        config.read("user.ini")

        for user_sec in config.sections():
            if config[user_sec]["username"] == username and config[user_sec]["password"] == password:
                print("auth ok for %s:%s" %(username, password))
                return True

        return False

    def login(self, cmd_dict):
        if self.auth(cmd_dict["username"], cmd_dict["password"]):
            self.request.sendall("auth suc".encode("utf-8"))
        else:
            self.request.sendall("auth failed".encode("utf-8"))

    def show(self):
        pass

    def handle(self):
        while True:
            cmd_line = self.request.recv(1024)
            if not cmd_line:
                continue

            cmd_dict = json.loads(cmd_line.decode())

            if hasattr(self, cmd_dict["action"]):
                func = getattr(self, cmd_dict["action"])
                func(cmd_dict)

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8888
    server = socketserver.ThreadingTCPServer((HOST, PORT), FtpServer)
    server.serve_forever()