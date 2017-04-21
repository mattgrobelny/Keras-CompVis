from PIL import Image
import glob
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pylab import *
import sys

# Dir for images
image_location = '/Users/matt/github/Keras-CompVis/data/one_cell/'
jpg = '*.TIF'

# string for glob to produce list of files only .jpgs
glob_dir = image_location + jpg
# print glob_dir

# Get list of images to work on
image_list = glob.glob(image_location + jpg)
# print image_list

# Filename for cell locations
outfile = 'Cell_locations.csv'

# output location
location_output = '/Users/matt/github/Keras-CompVis/data/one_cell_patches/'

out_fh = open(location_output + outfile, 'r')
lineList = out_fh.readlines()
out_fh.close()

done_files = []
for line in lineList:
    done_files.append(line.split(',')[0])


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
        imshow(self.img)
        print "Number of Clicks Left:", self.click_left

        # Trigger click detection
        self.cid_press = fig.canvas.mpl_connect(
            'button_press_event', self.__onclick__)

        # Annotate image with number of cells left to click
        ax.annotate(str(self.click_left), xy=(
            width * .9, height / 3), size=100, weight='bold', alpha=0.5)
        ax.annotate('Cells Left:', xy=(
            width * .8, height / 5), size=10, weight='bold', alpha=0.5)

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
    if image not in done_files:
        image_name = image.split('/')[-1][0:-4]
        cell_count_GT = int(image_name.split('_')[2].split('C')[1])

        print "Working on:", image_name, "--- %s" % (zero / len(image_list) * 100), '% done'

        click = Pixel_locator()
        click.fname = image
        click.click_left = cell_count_GT

        while click.click_left > 0:
            count = click.getCoord()
            click.point_list.append(count)
            print count
        else:
            cell_locations.append([image, click.point_list])

            # open outfile in append mode
            out_fh = open(location_output + outfile, 'a')

            # Write the Image name and location of cells to file
            out_fh.write("%s, %s\n" % (image_name, click.point_list))
            out_fh.close()
    else:
        continue
# print cell_locations
