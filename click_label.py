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

# Filename for cell locations change for image set you are working on
# CHANGE ME TO RUN SCRIPT
outfile = 'Cell_locations_200.csv'
# outfile = 'Cell_locations_500.csv'
# outfile = 'Cell_locations_1000.csv'

# output location - change for your directory
# CHANGE ME TO RUN SCRIPT
location_output = '/Users/matt/github/Keras-CompVis/data/cell_locations_out/'

jpg = '*.TIF'

# string for glob to produce list of files only .jpgs
glob_dir = image_location + jpg
# print glob_dir

# Get list of images to work on
image_list = glob.glob(image_location + jpg)
# print image_list

try:
    out_fh = open(location_output + outfile, 'r')
    lineList = out_fh.readlines()
    out_fh.close()

    done_files = []
    for line in lineList:
        done_files.append(line.split(',')[0])
except IOError:
    done_files = []


class Pixel_locator():

    # init first variables
    def __init__(self):
        self.fname = 'image.jpg'
        self.point = ()
        self.point_list = []
        self.click_left = 3

    # point collection fucntion
    def __onclick__(self, click):
        self.point = (int(click.xdata), int(click.ydata))
        self.click_left -= 1
        return self.point

    # point collections and image display function
    def getCoord(self):
        self.img = Image.open(self.fname)
        width, height = self.img.size
        fig = plt.figure()
        ax = fig.add_subplot(111)
        imshow(self.img, cmap='gray')
        print "Number of Clicks Left:", self.click_left

        # Trigger click detection
        self.cid_press = fig.canvas.mpl_connect(
            'button_press_event', self.__onclick__)

        # Annotate image with number of cells left to click
        ax.annotate(str(self.click_left), xy=(
            width, height / 3), size=30, weight='bold', alpha=0.9, color='red')
        ax.annotate('Cells Left:', xy=(
            width, height / 4), size=10, weight='bold', alpha=0.9, color='red')

        # Displace circle on clicked cells for a give image
        for shape in self.point_list:
            el = Ellipse(
                (shape[0], shape[1]), 20, 20, facecolor='r', alpha=0.5)
            ax.add_artist(el)
            el.set_clip_box(ax.bbox)

        plt.show(block=False)
        plt.waitforbuttonpress()
        return self.point

zero = 1

cell_locations = []
for image in image_list:
    image_name = image.split('/')[-1][0:-4]

    if image_name not in done_files:
        print "Working on:", image_name, "--- %s" % (float(zero + len(done_files)) / float(len(image_list)) * 100), '% done for image set'
        cell_count_GT = int(image_name.split('_')[2].split('C')[1])
        click = Pixel_locator()
        click.fname = image
        click.click_left = cell_count_GT

        while click.click_left > 0:
            count = click.getCoord()
            click.point_list.append(count)
            plt.close()
            print count
        else:
            cell_locations.append([image, click.point_list])

            # open outfile in append mode
            out_fh = open(location_output + outfile, 'a')

            # Write the Image name and location of cells to file
            out_fh.write("%s, %s\n" % (image_name, click.point_list))
            out_fh.close()
            print "Saved Data"
    else:
        zero += 1
        continue
