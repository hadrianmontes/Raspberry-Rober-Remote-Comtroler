import pygame
import socket
import subprocess
global vlc, shh1, ssh2

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    # Button 0 -> square
    # Button 1 -> cross
    # Button 2 -> circle
    # Button 3 -> triangle
    # Button 4 -> L1
    # Button 5 -> R1
    # Button 6 -> L2
    # Button 7 -> R2
    # Button 8 -> share
    # Button 9 -> options
    # Button 10 -> L3
    # Button 11 -> R3
    # Button 12 -> PS
    # BUtton 13 -> touchpad

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.x=0
        self.y=0

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value,2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value

        axis=self.axis_data

        if 0 in axis:
            self.x=axis[0]
            self.y=-axis[1]

        # Turbo
        if self.button_data[7]:
            self.x*=2
            self.y*=2
        # Start Camera
        if self.button_data[3]:
            subprocess.Popen(["firefox",otraip+"/html"],
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            return "camera"

        # Measure
        if self.button_data[1]:
            return "measure"
        if self.button_data[0]:
            return "light"

        # Exit
        if self.button_data[2]:
            return "exit"
        return "move "+str(self.x)+" "+str(self.y)+"\n"

if __name__=="__main__":
    global ps4
    ps4 = PS4Controller()
    ps4.init()

    global otraip
    otraip = "192.168.0.19"

    HOST, PORT = otraip, 9999
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        info = ps4.listen()
        if info == "exit":
            sock.sendall(info)
            received = sock.recv(1024)
            break
        sock.sendall(info)
        received = sock.recv(1024)
    sock.close()
