import sys
import Robot
import SocketServer
import RPi.GPIO as GPIO
import time
import subprocess
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    The orders acepted are:
    move xspeed yspeed
    """

    def handle(self):
        global encendido
        self.data = self.request.recv(1024).split()
        command = self.data[0]
        if command == "move":
            self.move_robot()
        elif command == "undo":
            self.undo_robot()
        elif command == "camera":
            subprocess.Popen(["su","-c",
                              '"/home/hadrian/Documentos/RPi_Cam_Web_Interface/start.sh"',
                              "hadrian"])
        elif command == "exit":
            subprocess.Popen(["su","-c",
                              '"/home/hadrian/Documentos/RPi_Cam_Web_Interface/stop.sh"',
                              "hadrian"])
            self.data=["move","0","0"]
            self.move_robot()
        elif command == "measure":
            print robot.distance_sensor.distance()
        elif command == "light":
            print "light"
            if encendido:
                print "on"
                encendido = False
                GPIO.output(4,GPIO.LOW)
            else:
                print "off"
                encendido=True
                GPIO.output(4,GPIO.HIGH)
            
        # print self.data
        self.request.sendall("1")

    def move_robot(self):
        try:
            vx,vy=[int(float(i)*vmax) for i in self.data[1:]]
        except:
            vx, vy = 0, 0
        # vx/=2
        if abs(vx) < 20:
            vx=0
        if abs(vy) < 20:
            vy=0
        # print "moving at ",vx,vy
        robot.custom(vx,vy)


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4,GPIO.OUT)
except:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4,GPIO.OUT)
global encendido
encendido = False
GPIO.output(4,GPIO.LOW)
LEFT_TRIM = 0
RIGHT_TRIM = 0
# Max velocity of the robot (the max value is 255)
global vmax
vmax = 150
global robot
robot = Robot.Robot()

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
