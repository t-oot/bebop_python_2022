import socket
from threading import Thread
from sys import argv
import signal
import time

looping = False


def loop(c):
    global looping
    looping = True
    print("connecting to Bebop2")
    ##success = bebop.connect(10)
    success = True
    print("result:", success)

    if (success):
        print("connected to Bebop2!")
        # print(bebop.sensors.battery)
        print("sleeping")
        # bebop.smart_sleep(2)

        # bebop.ask_for_state_update()

        # set safe indoor parameters
        # bebop.set_max_tilt(5)
        # bebop.set_max_vertical_speed(1)

        # trying out the new hull protector parameters - set to 1 for a hull protection and 0 without protection
        # bebop.set_hull_protection(1)
        try:
            while True:
                print("receiving")
                ch = c.recv(4096).decode()
                print("received:", ch)
                if ch == "t":
                    print("take off")
                    bebop.safe_takeoff(10)

                elif ch == "w":
                    print("move front")
                    bebop.fly_direct(roll=0, pitch=50, yaw=0,
                                     vertical_movement=0, duration=1)
                elif ch == "s":
                    print("move back")
                    bebop.fly_direct(roll=0, pitch=-50, yaw=0,
                                     vertical_movement=0, duration=1)
                elif ch == "a":
                    print("move left")
                    bebop.fly_direct(roll=-50, pitch=0, yaw=0,
                                     vertical_movement=0, duration=1)
                elif ch == "d":
                    print("move right")
                    bebop.fly_direct(roll=50, pitch=0, yaw=0,
                                     vertical_movement=0, duration=1)

                elif ch == "W":
                    print("move up")
                    bebop.fly_direct(roll=0, pitch=0, yaw=0,
                                     vertical_movement=20, duration=0.5)
                elif ch == "S":
                    print("move down")
                    bebop.fly_direct(roll=0, pitch=0, yaw=0,
                                     vertical_movement=-20, duration=0.5)
                elif ch == "A":
                    print("move clockwise")
                    bebop.fly_direct(roll=0, pitch=0, yaw=25,
                                     vertical_movement=0, duration=1)
                elif ch == "D":
                    print("move conclockwise")
                    bebop.fly_direct(roll=0, pitch=0, yaw=-25,
                                     vertical_movement=0, duration=1)

                elif ch == "f":
                    print("flip")
                    bebop.flip(direction="front")

                elif ch == "l":
                    print("land")
                    bebop.safe_land(10)

                elif ch == "q" or len(ch) == 0:
                    print("end")
                    bebop.safe_land(10)
                    break
        except socket.error:
            print("socket error")
            bebop.safe_land(10)
        finally:
            looping = False
            c.close()

        print("DONE - disconnecting")
        bebop.smart_sleep(5)
        bebop.disconnect()


signal.signal(signal.SIGINT, signal.SIG_DFL)
##from pyparrot.Bebop import Bebop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8080
s.bind(('', port))  # socketに名前をつける
print("listening port:"+str(port))
s.listen(0)  # 接続待ち
while True:
    if looping:
        time.sleep(0.1)
    else:
        c, addr = s.accept()  # 接続要求の取り出し
        print("connected by", addr)
        Thread(target=loop, args=(c,)).start()
        time.sleep(0.1)

##bebop = Bebop(drone_type="Bebop2")
