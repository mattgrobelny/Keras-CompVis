from PIL import Image
import glob
# import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pylab import *
import sys


# Dir for cell images - change for your directory
# CHANGE ME TO RUN SCRIPT
image_location = '/Users/matt/github/Keras-CompVis/data/rand_200/'

patch_location = '/Users/matt/github/Keras-CompVis/data/rand_200/patches/'
# Filename for cell locations change for image set you are working on
# CHANGE ME TO RUN SCRIPT
cell_location_csv = 'Cell_locations_200.csv'
# outfile = 'Cell_locations_500.csv'
# outfile = 'Cell_locations_1000.csv'

# output location - change for your directory
# CHANGE ME TO RUN SCRIPT
location_cell_csv = '/Users/matt/github/Keras-CompVis/data/cell_locations_out/'

####################################################
# patch prep parameters

# expected cell dims
cell_w = 35
cell_h = 35

# try to make x num blank patches per image
none_cell_images_count = 10

# high end pixel vals allowed in blank image
exm_pix = 100

####################################################

# open csv
csv_fh = open(location_cell_csv + cell_location_csv, 'r')

# Method for extracting image name and cell location from csv
for line in csv_fh:

    # Save image name
    image_info = line.split(',')[0]
    image_name = image_info

    # make a list of cell locations
    cell_locations = line.split('[')

    # prep an empty set for crop bound ranges
    cell_image_crop_ranges = set()

    print image_name
    if 1 != len(image_name.split("w1")):
        # print cell_locations[1].split('),')
        count = 1
        none_count = 0
        # Load the original image:
        img = Image.open(image_location + image_name + ".TIF")

        height, width = img.size

        for location in cell_locations[1].split('),'):

            x, y = location.replace("(", "").replace(
                ")", "").replace("]", "").split(",")

            # Crop boundaries
            x1 = int(x) - cell_h / 2
            y1 = int(y) - cell_w / 2
            x2 = int(x) + cell_h / 2
            y2 = int(y) + cell_w / 2

            # Save crop range
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    cell_image_crop_ranges.add((x, y))

            # Crop to patch
            img2 = img.crop((x1, y1, x2, y2))

            # Save patch XC means cell present Y = 1 , N =0
            img2.save(patch_location + image_name +
                      "_Patch_" + str(count) + "_CX_1" + ".TIF")
            count += 1

        # Make blank images no more than none_cell_images_count times
        while none_count != none_cell_images_count:

            # get random values in range of image size
            rand_x = randint(1, height)
            rand_y = randint(1, width)
            # print rand_x, rand_y
            # test if random pixel is already part of cell crop range
            if (rand_x, rand_y) not in cell_image_crop_ranges:
                list_of_vals = set()

                # bounds for blanks
                B_x1 = int(rand_x) - cell_h / 2
                B_y1 = int(rand_y) - cell_w / 2
                B_x2 = int(rand_x) + cell_h / 2
                B_y2 = int(rand_y) + cell_w / 2
                B_x3 = int(rand_x) + cell_h / 2
                B_y3 = int(rand_y) - cell_w / 2
                B_x4 = int(rand_x) - cell_h / 2
                B_y4 = int(rand_y) + cell_w / 2

                # make list for blank endpoints
                list_of_vals = set(
                    ((B_x1, B_y1), (B_x2, B_y2), (B_x3, B_y3), (B_x4, B_y4)))

                # test if end points are in crop ranges
                if list_of_vals.issubset(cell_image_crop_ranges):
                    rand_x = randint(1, height)
                    rand_y = randint(1, width)
                    continue
                else:
                    # if not in range of crop than make a blank image
                    blank_img = img.crop((B_x1, B_y1, B_x2, B_y2))
                    none_count += 1

                    # Save images if overall intenisty is bellow 100
                    if blank_img.getextrema()[1] < exm_pix:
                        print "blank", blank_img.getextrema()
                        blank_img.save(patch_location + image_name +
                                       "_Patch_" + str(none_count) + "_CX_0_" + ".TIF")
                    else:
                        continue
            else:
                continue
    else:
        continue
