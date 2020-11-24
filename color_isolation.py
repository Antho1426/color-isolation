#!/usr/local/bin/python3.7





# color_isolation.py









## Setting the current working directory automatically
import os
project_path = os.getcwd() # getting the path leading to the current working directory
os.getcwd() # printing the path leading to the current working directory
os.chdir(project_path) # setting the current working directory based on the path leading to the current working directory




## Required packages
import cv2
import numpy as np
import matplotlib.pyplot as plt


## Initializations

# Reading the input picture
img = cv2.imread(project_path + '/' + 'test.png')  # Read directly as grayscale image

# Defining the class of the hsv_range_list object:
class hsvRangeList:
    def __init__(self, list):
        self.list = []
    def add_element(self, elem):
        self.list.append(elem)
    def get_elements(self):
        return self.list
hsv_range_list = hsvRangeList([])






## First operations

# Reducing the image (for easy display)
height, width = img.shape[:2]
height_display = 800 # setting a height of a desirable number of pixels
width_display = int(height_display * width / height) # proportional width
size = (width_display, height_display)
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

# Converting from BGR to HSV
frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Defining the main function for mouse click response event
# (cf.: https://www.programmersought.com/article/82483774170/)
def getposHsv(event, x, y, flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        # Appending the HSV values to the hsv_range_list
        hsv_range_list.add_element(frame_HSV[y, x])

        if len(hsv_range_list.get_elements()) <= 5:
            # Printing the HSV values
            print("HSV is",frame_HSV[y, x])

        # Computing the HSV range if enough (i.e. 5) HSV values in hsv_range_list
        if len(hsv_range_list.get_elements()) == 5:

            # Getting the list of recorded HSV values
            print("\nhsv_range_list.get_elements(): ", hsv_range_list.get_elements())
            print("hsv_range_list.get_elements()[0]: ", hsv_range_list.get_elements()[0])
            print("hsv_range_list.get_elements()[0][0]: ", hsv_range_list.get_elements()[0][0])

            # Computing the means of H, S and V values
            h1 = int(hsv_range_list.get_elements()[0][0])
            h2 = int(hsv_range_list.get_elements()[1][0])
            h3 = int(hsv_range_list.get_elements()[2][0])
            h4 = int(hsv_range_list.get_elements()[3][0])
            h5 = int(hsv_range_list.get_elements()[4][0])
            h_mean = int((h1 + h2 + h3 + h4 + h5) / 5)
            print("\nh_mean: ", h_mean)
            s1 = int(hsv_range_list.get_elements()[0][1])
            s2 = int(hsv_range_list.get_elements()[1][1])
            s3 = int(hsv_range_list.get_elements()[2][1])
            s4 = int(hsv_range_list.get_elements()[3][1])
            s5 = int(hsv_range_list.get_elements()[4][1])
            s_mean = int((s1 + s2 + s3 + s4 + s5) / 5)
            print("s_mean: ", s_mean)
            v1 = int(hsv_range_list.get_elements()[0][2])
            v2 = int(hsv_range_list.get_elements()[1][2])
            v3 = int(hsv_range_list.get_elements()[2][2])
            v4 = int(hsv_range_list.get_elements()[3][2])
            v5 = int(hsv_range_list.get_elements()[4][2])
            v_mean = int((v1 + v2 + v3 + v4 + v5) / 5)
            print("v_mean: ", v_mean)

            # Computing the HSV range
            range_width_h = 70
            range_width_s = 90
            range_width_v = 70
            h_min = int(h_mean - range_width_h/2)
            if h_min < 0:
                h_min = 0
            h_max = int(h_mean + range_width_h/2)
            if h_max > 179:
                h_max = 179
            s_min = int(s_mean - range_width_s/2)
            if s_min < 0:
                s_min = 0
            s_max = int(s_mean + range_width_s/2)
            if s_max > 255:
                s_max = 255
            v_min = int(v_mean - range_width_v/2)
            if v_min < 0:
                v_min = 0
            v_max = int(v_mean + range_width_v/2)
            if v_max > 255:
                v_max = 255
            print("\nh range: [{0}, {1}]".format(h_min, h_max))
            print("s range: [{0}, {1}]".format(s_min, s_max))
            print("v range: [{0}, {1}]".format(v_min, v_max))

            # Creating and displaying the mask
            mask = cv2.inRange(frame_HSV, (h_min, s_min, v_min), (h_max, s_max, v_max))
            cv2.imshow("frame_threshold", mask)

            # Creating the final frame by colorizing only the region of interest
            # Converting the whole image into a 3 channels grayscaled image
            frame_gray_1_channel = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            frame_gray_3_channels = cv2.cvtColor(frame_gray_1_channel, cv2.COLOR_GRAY2BGR)

            # Applying the mask on the input picture to retrieve only the
            # colorized object of interest
            frame_color_extracted = cv2.bitwise_and(img, img, mask=mask)

            # Black-outing the area of interest from the grayscaled image
            mask_inv = cv2.bitwise_not(mask)
            frame_gray_3_channels_colored_region_removed = cv2.bitwise_and(frame_gray_3_channels, frame_gray_3_channels, mask=mask_inv)

            # Adding colorized object to the grayscaled version of the input image
            frame_output = cv2.add(frame_color_extracted,frame_gray_3_channels_colored_region_removed)

            # Showing up the resulting image
            cv2.imshow("frame_output", frame_output)

            # Saving the frame_output picture
            cv2.imwrite(project_path + '/results/' + 'output_opencv.png', frame_output)

            # Generating the "Color isolation process" picture
            Fig = plt.figure(figsize=(9, 6))
            Fig.suptitle('Color isolation process', fontsize=14, fontweight='bold')
            # frame_input
            Fig.add_subplot(2, 2, 1)
            img_matplotlib = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img_matplotlib)
            plt.title('frame_input')
            # frame_HSV
            Fig.add_subplot(2, 2, 2)
            frame_HSV_matplotlib = cv2.cvtColor(frame_HSV, cv2.COLOR_BGR2RGB)
            plt.imshow(frame_HSV_matplotlib)
            plt.title('frame_HSV')
            # frame_threshold
            Fig.add_subplot(2, 2, 3)
            frame_threshold_matplotlib = cv2.cvtColor(mask, cv2.COLORMAP_AUTUMN)
            plt.imshow(frame_threshold_matplotlib)
            plt.title('frame_threshold')
            # frame_output
            Fig.add_subplot(2, 2, 4)
            frame_output_matplotlib = cv2.cvtColor(frame_output, cv2.COLOR_BGR2RGB)
            plt.imshow(frame_output_matplotlib)
            plt.title('frame_output')
            plt.tight_layout(pad=1.2, h_pad=None, w_pad=None, rect=None)
            # Saving the generated picture
            plt.savefig(project_path + '/results/' + 'colorIsolationProcess.png')
            plt.show()


# Displaying the HSV version of the picture
cv2.imshow("frame_HSV", frame_HSV)

# Setting up the mouse callbacks to be able to retrieve HSV values when clicking
# on the HSV version of the picture
cv2.setMouseCallback("frame_HSV", getposHsv)

# We can escape the program at any time by clicking any key we want
cv2.waitKey(0)
cv2.destroyAllWindows()



