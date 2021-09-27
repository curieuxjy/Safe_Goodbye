import cv2
import numpy as np
import serial
import time

arduino=serial.Serial('COM5', 9600)
while True:
    c=input()
    c=c.encode('utf-8')
    arduino.write(c)