import socket
import sys
#import termios
#import tty
import msvcrt


class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


def send_to(t):
    if t == 0:
        print("Send to all drones. Send q to quit.")
        while True:
            print("All drones > ", end="", flush=True)
            command = msvcrt.getch()
            try:
                command_ = command.decode('UTF-8')
            except:
                command_ = "0x"+command.hex()
                continue
            #command = sys.stdin.read(1)
            if command_ == "c":
                break
            i = 1
            for s in sockets:
                s.send(command)
                print(command_ + " > " + Color.GREEN +
                      "[drone "+str(i)+"]" + "sent.", Color.END, flush=True)
                i += 1
            if command_ == "q":
                break
    elif t <= 3:
        print("Send to drone %s  Send q to quit." % target)
        while True:
            print("drone", target, "> ", end="", flush=True)
            command = msvcrt.getch()
            try:
                command_ = command.decode('UTF-8')
            except:
                command_ = "0x"+command.hex()
                continue
            if command_ == "c":
                break
            sockets[t-1].send(command)
            print(command_ + " > " + Color.GREEN +
                  "sent.", Color.END, flush=True)
            if command_ == "q":
                break
    else:
        return


#fd = sys.stdin.fileno()
#old = termios.tcgetattr(fd)
sockets = []

hosts = ["192.168.1.1", "192.168.1.2"]
#hosts = ["127.0.0.1"]
port = 8080
nodelay = 1

i = 1
for h in hosts:
    print(Color.YELLOW+"[drone "+str(i)+"]connecting host:",
          h, " port:", port, Color.END)
    sock = socket.socket()
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, nodelay)
    sock.connect((h, port))
    sockets.append(sock)
    print(Color.GREEN + "[drone "+str(i)+"]connected host:",
          h, " port:", port, Color.END)
    i += 1


try:
    # tty.setcbreak(sys.stdin.fileno())
    while True:
        print("select target(1~3). 0:all 9:end\n>", end="")
        target = sys.stdin.readline()  # 1文字読み込み
        target = target.strip()
        if target.isdecimal():  # 入力が数字かどうか判定
            if int(target) == 9:
                print("end")
                command = "q"
                for s in sockets:
                    s.send(command.encode('utf-8'))
                break
            else:
                send_to(int(target))
            print("end")
            command = "q"
            for s in sockets:
                s.send(command.encode('utf-8'))
            break
        else:
            print(Color.RED+"invalid literal!", Color.END)

finally:
    pass
    #termios.tcsetattr(fd, termios.TCSANOW, old)

print("end client")
