import os
import pygame
import socket
import atexit
import subprocess
global vlc, shh1, ssh2
import time
import sys
def close():
    ssh1.kill()
    vlc.kill()
    ssh2.kill()
    pass


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

            # Insert your code on what you would like to happen for each event here!
            # In the current setup, I have the state simply printing out to the screen.

        os.system('clear')

        axis=self.axis_data
        if not axis:
            return self.x,self.y
        if 0 in axis:
            self.x=axis[0]
        if 1 in axis:
            self.y=-1*axis[1]
        if self.button_data[7]:
            self.x*=2
            self.y*=2
        return self.x,self.y
        # pprint.pprint()

if __name__=="__main__":
    global ps4
    ps4 = PS4Controller()
    ps4.init()

    atexit.register(close)

    f = os.popen('ifconfig wlp4s0 | grep "inet" | cut -d: -f2 | cut -d" " -f1')
    myip=f.read().strip()
    otraip=sys.argv[1]

    print "Conectando la camara del robot"
    ssh2=subprocess.Popen(["ssh",otraip,"python","test_camera_stream.py"],stdout=subprocess.PIPE)
    time.sleep(0.5)

    print "Conectando Controles"
    ssh1=subprocess.Popen(["ssh",otraip,"sudo","python","acorrer2.py",myip],stdout=subprocess.PIPE)
    time.sleep(0.5)

    print "Conectando al stream"

    string="tcp/h264://"+otraip+":8000/"
    vlc=subprocess.Popen(["vlc",string],stdout=subprocess.PIPE)
