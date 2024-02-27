# ESE498_Object_Detection

# Mingkang You, Sicheng Yang, Lily Fu

# Citation: https://www.geeksforgeeks.org/detect-an-object-with-opencv-python/

import cv2
from matplotlib import pyplot as plt
   
# Opening image.
img = cv2.imread("StopSign2.jpg")
   
#Get the grayscale version and RGB version of picture.
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   
   
# Use minSize to avoid extra small object that looks alike a stop sign.
data = cv2.CascadeClassifier('StopSign.xml')   
found = data.detectMultiScale(imgGray, minSize = (100, 100))   

amountfound = len(found)
# Judge whether we find any stop sign.  
if amountfound != 0:       

    for (x, y, width, height) in found:
           
        # We draw a green rectangle around every recognized stop sign.
        cv2.rectangle(imgRgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
           
# Plot the new picture.
plt.subplot(1, 1, 1)
plt.imshow(imgRgb)
plt.show()