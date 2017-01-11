import sys
import Robot
import SocketServer
import time
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    The orders acepted are:
    move xspeed yspeed
    undo
    """

    def __init__(self,*args,**kwargs):
        super(MyTCPHandler, self).__init__(*args,**kwargs)
        self.move_history=[]
        self.last_move=None
        self.last_move_start=0
        self.robot = robot

    def handle(self):
        self.data = self.rfile.readline().split()
        command = self.data[0]
        print command
        if command == "move":
            self.move_robot()
        elif command == "undo":
            self.undo_robot()
        print self.data
        self.request.sendall(self.data.upper())

    def move_robot(self):
        x, y = self.data[1:]
        try:
            vx,vy=[int(float(i)*vmax) for i in self.data[1:].split()]
        except:
            vx, vy = 0, 0
        vx/=2
        if abs(vx) < 20:
            vx=0
        if abs(vy) < 20:
            vy=0

        if self.last_move is not None:
            self.move_history.append(time.time()-self.last_move_start,self.last_move)
        self.last_move_start = time.time()
        self.last_move = (vx, vy)
        print "moving to ",vx,vy
        self.robot.custom(vx,vy)

    def undo_robot(self):
        if len(self.move_history) == 0:
            return
        vx, vy = self.move_history.pop()[1]
        self.robot.custom(-vx,-vy)


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
