import sys
import Robot
import SocketServer
import time
import subprocess
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    The orders acepted are:
    move xspeed yspeed
    """

    def handle(self):
        self.data = self.request.recv(1024).split()
        command = self.data[0]
        if command == "move":
            self.move_robot()
        elif command == "undo":
            self.undo_robot()
        elif command == "camera":
            subprocess.Popen("~/Documentos/RPi_Cam_Web_Interface/start")
        elif command == "exit":
            subprocess.Popen("~/Documentos/RPi_Cam_Web_Interface/stop")
            self.data=["move","0","0"]
            self.move_robot()
        print self.data
        self.request.sendall("1")

    def move_robot(self):
        try:
            vx,vy=[int(float(i)*vmax) for i in self.data[1:]]
        except:
            vx, vy = 0, 0
        vx/=2
        if abs(vx) < 20:
            vx=0
        if abs(vy) < 20:
            vy=0
        print "moving at ",vx,vy
        robot.custom(vx,vy)


LEFT_TRIM = 0
RIGHT_TRIM = 0
# Max velocity of the robot (the max value is 255)
global vmax
vmax = 150
global robot
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Create the server, binding to localhost on port 9999
HOST, PORT = "", 9999
server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()



# HOST, PORT = sys.argv[1], 9999

# while True:
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.connect((HOST, PORT))
#         sock.sendall("a\n")
#         received = sock.recv(1024)
#         vx,vy=[int(float(i)*vmax) for i in received.split()]
#     except:
#         vx=0
#         vy=0
#     vx/=2.
#     # print vx, vy
#     if abs(vx) < 10:
#         vx=0
#     if abs(vy) < 10:
#         vy=0
# #    print vx, vy
#     sock.close()
#     # time.sleep(0.1)
#     robot.custom(vx,vy)
# #    print vx, vy
# #    time.sleep(0.5)
