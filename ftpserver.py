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
            welcome = "welcome to ftpserver %s" % cmd_dict["username"]
            self.pwd = os.getcwd()
            self.pwd += '/'
            self.homedir = cmd_dict["username"]
            if not os.path.exists(self.pwd+self.homedir):
                os.mkdir(self.pwd+self.homedir)

            self.curdir = self.homedir
            os.chdir(self.pwd+self.curdir)

            msg_dict = {"ret":True, "cur_dir":self.curdir}
            self.request.sendall(json.dumps(msg_dict).encode("utf-8"))

        else:
            msg_dict = {"ret":False}
            self.request.sendall("auth failed".encode("utf-8"))

    def show(self, cmd_dict):
        file_list = os.listdir(self.pwd + self.curdir)
        file_str = ''
        for file in file_list:
            file_str += (file + ' ')

        self.request.sendall(file_str.encode('utf-8'))

    def cd(self, msg_dict):
        chdir = msg_dict["dir"]
        suc = False

        if chdir == ".":
            suc = True
        elif chdir == "..":
            if 1 < len(self.curdir.split("\\")):
                self.curdir = self.curdir.rsplit("\\", 1)[0]
                os.chdir(self.pwd+self.curdir)
                suc = True
            else:
                print("already in the home dirtory")
        else:
            ab_chdir = self.pwd+self.curdir+'\\'+chdir
            if os.path.exists(ab_chdir):
                os.chdir(self.pwd+self.curdir+'\\'+chdir)
                self.curdir = self.curdir+'\\'+chdir
                suc = True
            else:
                pass

        if suc == True:
            msg_dict = {"ret":True, "cur_dir":self.curdir}
            self.request.sendall(json.dumps(msg_dict).encode('utf-8'))
        else:
            msg_dict = {"ret":False}
            self.request.sendall(json.dumps(msg_dict).encode('utf-8'))

    def makedir(self, msg_dict):
        if not os.path.exists(self.curdir + msg_dict["dir"]):
            os.mkdir(msg_dict["dir"])
            self.request.sendall("make dir succ".encode('utf-8'))
        else:
            self.request.sendall("make dir failed!".encode('utf-8'))

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