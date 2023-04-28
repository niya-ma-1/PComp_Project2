from gpiozero import MotionSensor, LED
import RPi.GPIO as GPIO
import pigpio
import time
import pygame
import socket

GPIO.setmode(GPIO.BCM)

knock_sensor = 26
GPIO.setup(knock_sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)

start = time.time()

curr_password = [0]

password = [3,2,1]

#Function executed on signal detection
def active(void):
    global start 
    end = time.time()
    if end-start < 1.3:
        curr_password[-1] = curr_password[-1] + 1
    else:
        curr_password.append(1)
    print(curr_password)
    start = time.time()

def signal():

    print('signal')
    time.sleep(1)

    HOST = '10.53.134.70'  # The IP address of the machine running the listening program
    PORT = 12345  # The same port number that the listening program is listening on

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server on the specified port
    s.connect((HOST, PORT))

    # send some data to the server
    s.sendall(b'Hello, server!')

    # receive some data from the server
    data = s.recv(1024)

    # print the data that was received
    print('Received', repr(data))

    # close the connection
    s.close()

def checkpassword():
    print(curr_password)
    if curr_password[-3:] == password:
        print("you got it!")
        return 1
    else: return 0

pi = pigpio.pi()
LIGHT_STRIP_PIN = 17

motion = False
def defense(void):
    global motion
    motion = True
    
    try:
        signal()
    except:
        print("signal failed")

    pygame.mixer.init()
    sound = pygame.mixer.Sound('alarm.wav')
    sound.play()

motion_sensor = 4
GPIO.setup(motion_sensor, GPIO.IN)

GPIO.add_event_detect(motion_sensor, GPIO.RISING, callback=defense)

#On detecting signal (falling edge), active function will be activated.
GPIO.add_event_detect(knock_sensor, GPIO.FALLING, callback=active, bouncetime=100) 

# main program loop
while True:
    if not motion:
        continue
    if checkpassword() == 1:
        break
    pi.set_PWM_dutycycle(17, 255)
    print('on')
    time.sleep(0.7)
    pi.set_PWM_dutycycle(17, 0) 
    time.sleep(0.7)
