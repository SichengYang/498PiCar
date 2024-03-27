import argparse
import time
from picar import PiCar     
import matplotlib as matlib
import matplotlib.pyplot as plt
import numpy as np

# return real time speed if detected a transition
# return -1 if no transition is found
def calculate_speed(ch1_data):
    average_data= sum(ch1_data)/ len(ch1_data)
    transition = 0
    above_count = 0
    below_count = 0
    for element in ch1_data:
        #print(f'{element},{average_data}')
        if abs(element-average_data) > 10:
            if element < average_data:
                below_count += 1
            else:
                above_count += 1

        # one transition occur
        if(below_count >= 2 and above_count >= 2):
            transition += 1
            if(below_count > above_count):
                below_count = 0
            else:
                above_count = 0
    return transition /4 / 0.66

parser = argparse.ArgumentParser (description='Data for this program. ')
parser.add_argument ('--tim', action='store', type=float, default=10, help='loop time')
parser.add_argument ('--delay', action='store', type=float, default=0.01, help='delay between sample')
parser.add_argument ('--rps', action='store', type=float, default=3, help='ramp per second')
parser.add_argument ('--Kp', action='store', type=float, default=0.9, help='Kp')
parser.add_argument ('--Ki', action='store', type=float, default=0.06, help='Ki')
parser.add_argument ('--Kd', action='store', type=float, default=0, help='Kd')
parser.add_argument ('--debug' , action='store_true', default = False, help='specifies if debug statements are printed')
args = parser.parse_args()

time_data = [0] * int(0.66/args.delay+ 1)
ch1_data = [0] * int(0.66/args.delay+ 1)

if args.debug:
    # Print nice channel column headers.
    print(" time | ch 1|")
    print('-' * 57)

car = PiCar(mock_car = False, threaded=False)
enable = False
counter = 0
index = 0
error = [0] * int(args.tim/args.delay+ 1)
startTime= time.time()
loopTime= startTime+ args.tim
timeCounter=startTime
duty = (args.rps) / 0.0485

file = open("car_noload_3rps.txt", "w")
file.write(f"{args.delay}\n")

while time.time()< loopTime:
    if time.time() >= timeCounter:        
        if(time.time() - startTime >= 1 and enable == False):
            car.set_motor(duty)
            enable = True
        
        values = car.adc.read_adc(0)
        print(values)
        record_time = round(timeCounter-startTime, 3)
        time_data[counter] = record_time
        ch1_data[counter] = values

        if(time.time() - startTime >= 1):
            speed = calculate_speed(ch1_data)
        
            error[index] = args.rps - speed

            sum_error = 0
            for i in range(0,index):
                sum_error += error[index]

            new_duty = duty + args.Kp*error[index] + args.Ki * sum_error + args.Kd * (error[index]-error[index-1])
            
            print(f"New duty:{new_duty} time:{time.time()-startTime} speed:{speed} error:{error[index]} sum err:{sum_error}")
            file.write(f"{time.time()-startTime:.4f}\t{values}\t{speed:.3f}\n")
            
            if(new_duty > 100):
                new_duty = 100
            elif(new_duty < 0):
                new_duty = duty
            
            car.set_motor(new_duty)

            index += 1
        else:
            file.write(f"{time.time()-startTime:.4f}\t{values}\t0.000\n")

        counter += 1
        timeCounter += args.delay

        if args.debug:
            # Print the ADC values.
            print(f'{record_time:>5}| {values:>4}|')
        
        if counter == int(0.66 /args.delay):
            counter = 0


file    = open("car_noload_3rps.txt", 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False                     # For printing debug statements

time    = [0]*MAXSIZE
photo   = [0]*MAXSIZE

for line in range (1, MAXSIZE):
    values   = data[line].split()   # split on white space
    time[line]  = float(values[0])     # first item in file is time
    photo[line] = float(values[2])       # second is the value
    if DEBUG: print (f'{i}\t{time[i]}\t{photo[i]}')

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

plt.plot(time, photo)
plt.xlabel('time - sec')
plt.ylabel('velocity - rps')
plt.savefig('velocity.png')
