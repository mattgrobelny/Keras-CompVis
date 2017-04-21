from PIL import Image
import glob
import cv2
import matplotlib.pyplot as plt

from PIL import Image
from pylab import *

# Dir for images
image_location = '/Users/matt/github/Keras-CompVis/data/one_cell/'
jpg = '*.TIF'

# string for glob to produce list of files only .jpgs
glob_dir = image_location + jpg
# print glob_dir

# Get list of images to work on
image_list = glob.glob(image_location + jpg)
# print image_list


# output location
image_location_output = '/Users/matt/github/Keras-CompVis/data/one_cell_patches'


class TestClass():

    def __init__(self):
        self.fname = 'image.jpg'
        self.point = ()
        self.point = ()
        self.point_list = []
        self.click_left = 3

    def __onclick__(self, click):
        self.point = (click.xdata, click.ydata)
        self.click_left -= 1
        return self.point

    def __on_Declick__(self, declick):
        self.fig.canvas.mpl_disconnect(self.cid_press)

    def getCoord(self):
        self.img = Image.open(self.fname)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        imshow(self.img)
        print self.click_left
        self.cid_press = fig.canvas.mpl_connect(
            'button_press_event', self.__onclick__)
        plt.show(block=False)
        plt.waitforbuttonpress()
        return self.point

list = []
zero = 1

cell_locations = []
for image in image_list[1:2]:

    image_name = image.split('/')[-1][0:-4]
    cell_count_GT = int(image_name.split('_')[2].split('C')[1])
    # cell_count_GT = 3

    print "Working on:", image_name, "--- %s" % (zero / len(image_list) * 100), '% done'

    click = TestClass()

    click.fname = image
    click.click_left = cell_count_GT

    # count = click.getCoord()
    # click.point_list.append(count)
    # print count
    #
    # cell_locations = click.point_list

    while click.click_left > 0:
        count = click.getCoord()
        click.point_list.append(count)
        print count
    else:
        cell_locations = click.point_list
print cell_locations
