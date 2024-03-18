from picar import PiCar
import cv2
import numpy as np
import math
import time 
import argparse
from picamera import PiCamera 
import picamera.array
from functions import calculate_speed
import matplotlib as matlib
import matplotlib.pyplot as plt

def blue (image, debug=False) :
    x = -100
    y = -100
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert to hsv
    
    mask = cv2.inRange(hsv, (100, 0, 0), (150, 255, 255)) # filter blue

    mask_blur = cv2.blur(mask,(5,5))
    thresh = cv2.threshold(mask_blur, 200, 255, cv2.THRESH_BINARY)[1]
    
    M = cv2.moments(thresh)
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"]) 
        y = int(M["m01"] / M["m00"])
        
    return x,y

# reae command line arguments
parser = argparse. ArgumentParser (description='Data for this program. ')
parser .add_argument ('--tim', action='store', type=int, default=10, help='total run time')
parser.add_argument ('--delay', action='store', type=float, default=0.01, help='delay between sample')
parser.add_argument ('--Kp', action='store', type=float, default=1.1, help='Kp')
parser.add_argument ('--Ki', action='store', type=float, default=0.01, help='Ki')
parser.add_argument ('--Kd', action='store', type=float, default=0, help='Kd')
parser .add_argument ('--debug' , action='store_true', default = True, help='specifies if debug statements are printed')
parser .add_argument ('--delta' , action='store', type=float, default = 7, help='delta')
parser.add_argument('--rps', action='store',type=float, help='rps')
args = parser.parse_args()

car= PiCar(mock_car = False, threaded=False)

x_dutycycle = 0
y_dutycycle = 0

car.set_swivel_servo(x_dutycycle)
car.set_steer_servo(x_dutycycle)
car.set_nod_servo(y_dutycycle)

# set up camera
camera = PiCamera()
camera. framerate = 30
stream = picamera.array.PiRGBArray(camera) # Create the stream
camera.resolution = (320, 208)
time_count = 0
period = 0.66
time_data = [0] * int(period/args.delay+ 1)
ch1_data = [0] * int(period/args.delay+ 1)
counter = 0
index = 0
error = [0] * int(args.tim/args.delay+ 1)
startTime= time.time()
loopTime= startTime+ args.tim
timeCounter=startTime
duty = 0
run = True
filename = "object3-" +  f'{args.rps}' + ".txt"
data_file = open(filename, "w")

stop = 0
if args.rps <= 3.5:
    stop = math.sqrt(args.rps) * 7 + 80
elif args.rps <= 4.5:
    stop = args.rps * 12 + 70
elif args.rps <= 5:
    stop = args.rps * args.rps * 9
else:
    stop = args.rps * args.rps * 7.5

while time.time()-startTime < args.tim:
    # take picture
    camera.capture(stream, format= 'bgr', use_video_port=True)
    image = stream.array
    stream.truncate(0)
    x,y = blue(image, True)
    
    if x != -100:
        x_dutycycle -= args.delta * (x - 160)/ 160

        if(x_dutycycle > -10 and x_dutycycle < 10):
            car.set_swivel_servo(x_dutycycle)
            car.set_steer_servo(x_dutycycle)
        elif x_dutycycle < -10:
            x_dutycycle = -10
        elif x_dutycycle > 10:
            x_dutycycle = 10

    if time.time() >= time_count:        
        
        distance = car.read_distance()
        
        # Update the duty cycle.
        if distance< stop:
            duty= 0
            run = False
        elif run and distance<= 1000:
            duty= args.rps/0.1
            if duty > 100:
                duty = 100
        elif distance> 1000:
            duty= 0

        values = car.adc.read_adc(0)
        record_time = round(time_count-startTime, 3)
        time_data[counter] = record_time
        ch1_data[counter] = values

        speed = calculate_speed(ch1_data, args.rps)
        
        curr_time = time.time()-startTime
        data_file.write(f'{curr_time}\t{speed}\n')

        if args.debug:
            print(f'time: {curr_time}\tspeed: {speed}\n')
        
        error[index] = duty - speed

        sum_error = 0
        for i in range(0,index):
            if error[index] < 1.5:
                sum_error += error[index]
        
        new_duty = duty + args.Kp*error[index] + args.Ki * sum_error + args.Kd * (error[index]-error[index-1])
            
            
        if(new_duty > 100):
            new_duty = 100
        elif(new_duty < 0):
            new_duty = duty

        car.set_motor(new_duty)

        index += 1

        counter += 1
        
        if counter == int(period /args.delay):
            counter = 0

    time.sleep(args.delay)
    time_count += args.delay

data_file.close()

file = open(filename, 'r')
data = file.read().splitlines()
maxsize = len(data)

time = [0]*maxsize
photo = [0]*maxsize

for line in range (0,maxsize):
    values = data[line].split()
    time[line] = float(values[0])
    photo[line] = float(values[1])

xmarks = np.linspace(time[0], time[maxsize - 1], 5)

plt.xticks(xmarks)
plt.plot(time, photo)
plt.xlabel('time - sec')
plt.ylabel('velocity - rps')

png_name = 'velocity' + f'{args.rps}'+ '.png'
plt.savefig(png_name)
