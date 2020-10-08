import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

import cv2
import numpy as np

class WebcamVideoStream:
    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target = self.update, args = ()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

GPIO.setmode(GPIO.BOARD)

lm_ena = 33
lm_pos = 35
lm_neg = 37

rm_ena = 36
rm_pos = 38
rm_neg = 40

GPIO.setup(lm_ena,GPIO.OUT)
GPIO.setup(lm_pos,GPIO.OUT)
GPIO.setup(lm_neg,GPIO.OUT)

GPIO.setup(rm_ena,GPIO.OUT)
GPIO.setup(rm_pos,GPIO.OUT)
GPIO.setup(rm_neg,GPIO.OUT)

def moveRobot(direction):
    if (direction == 'f'):
        print('Forward')
        
        # Left Motor Forward
        GPIO.output(lm_ena,GPIO.HIGH)
        GPIO.output(lm_pos,GPIO.HIGH)
        GPIO.output(lm_neg,GPIO.LOW)

        # Right Motor Forward
        GPIO.output(rm_ena,GPIO.HIGH)
        GPIO.output(rm_pos,GPIO.HIGH)
        GPIO.output(rm_neg,GPIO.LOW)

    if (direction == 'b'):
        print('Backward')
        
        # Left Motor Backward
        GPIO.output(lm_ena,GPIO.HIGH)
        GPIO.output(lm_pos,GPIO.LOW)
        GPIO.output(lm_neg,GPIO.HIGH)

        # Right Motor Backward
        GPIO.output(rm_ena,GPIO.HIGH)
        GPIO.output(rm_pos,GPIO.LOW)
        GPIO.output(rm_neg,GPIO.HIGH)

    if (direction == 'r'):
        print('Right')
        
        # Left Motor Forward
        GPIO.output(lm_ena,GPIO.HIGH)
        GPIO.output(lm_pos,GPIO.HIGH)
        GPIO.output(lm_neg,GPIO.LOW)

        # Right Motor Backward
        GPIO.output(rm_ena,GPIO.HIGH)
        GPIO.output(rm_pos,GPIO.LOW)
        GPIO.output(rm_neg,GPIO.HIGH)

    if (direction == 'l'):
        print('Left')
        
        # Left Motor Backward
        GPIO.output(lm_ena,GPIO.HIGH)
        GPIO.output(lm_pos,GPIO.LOW)
        GPIO.output(lm_neg,GPIO.HIGH)

        # Right Motor Forward
        GPIO.output(rm_ena,GPIO.HIGH)
        GPIO.output(rm_pos,GPIO.HIGH)
        GPIO.output(rm_neg,GPIO.LOW)

    if (direction == 's'):
        print('Stop')
        
        # Left Motor Stop
        GPIO.output(lm_ena,GPIO.HIGH)
        GPIO.output(lm_pos,GPIO.LOW)
        GPIO.output(lm_neg,GPIO.LOW)

        # Right Motor Stop
        GPIO.output(rm_ena,GPIO.HIGH)
        GPIO.output(rm_pos,GPIO.LOW)
        GPIO.output(rm_neg,GPIO.LOW)

cam = WebcamVideoStream(src=0).start()

while(True):
    # Capture frame-by-frame
    frame = cam.read()
    # Display the resulting frame

    key = cv2.waitKey(10)
    
    if key == ord('w'):
        moveRobot('f')

    if key == ord('a'):
        moveRobot('l')

    if key == ord('s'):
        moveRobot('b')

    if key == ord('d'):
        moveRobot('r')

    if key == 32:
        moveRobot('s')

    if key == 27:         # wait for ESC key to exit
        break

    cv2.imshow('frame',frame)

# When everything done, release the capture
cam.stop()
cv2.destroyAllWindows()
GPIO.cleanup()
