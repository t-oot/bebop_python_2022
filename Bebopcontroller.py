import socket
from threading import Thread
from sys import argv
import signal
import time
from pyparrot.Bebop import Bebop

looping = False


def loop(c):

    c.settimeout(1)
    c.setblocking(0)
    while True:
        try:
            global looping
            looping = True
            bebop = Bebop(drone_type="Bebop2")
            print("connecting to Bebop2")
            success = bebop.connect(10)
            #success = True
            print("result:", success)
        except:
            looping=False
            c.close()
            return

        if (success):
            c.settimeout(3600)
            c.setblocking(1)
            print("connected to Bebop2!")
            print("battery level:", bebop.sensors.battery)
            print("sleeping")
            bebop.smart_sleep(2)
            print("step1/4")
            bebop.ask_for_state_update()
            print("step2/4")
            # set safe indoor parameters
            bebop.set_max_tilt(5)
            print("step3/4")
            try:
                bebop.set_max_vertical_speed(1)
            except Exception as e:
                print(e)
            print("step4/4")
            # trying out the new hull protector parameters - set to 1 for a hull protection and 0 without protection
            #bebop.set_hull_protection(1)
            try:
                while True:
                    print("receiving")
                    ch = c.recv(1).decode()
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
                        looping=False
                        break
            except socket.error as ee:
                print("socket error",ee)
                bebop.safe_land(10)
                looping = False
                c.close()
            except Exception as e:
                print("bebop error")
                print(e)
            finally:
                pass

            print("DONE - disconnecting")
            bebop.smart_sleep(5)
            bebop.disconnect()
            if not looping:
                break
        else:
            print("waiting 1sec")
            try :
                ch = c.recv(1024).decode()
                if ch=="":
                    looping=False
                    break
                print("recv:",str(ch))
                print("break")
                looping = False
                c.close()
                break
            except:
                pass
    print("loop end")
        


signal.signal(signal.SIGINT, signal.SIG_DFL)
# from pyparrot.Bebop import Bebop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 1)
#s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 5000))
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
        c.send("ok".encode("utf-8"))
        Thread(target=loop, args=(c,)).start()
        time.sleep(0.1)