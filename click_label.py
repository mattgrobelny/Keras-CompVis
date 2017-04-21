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


# class TestClass():
#
#     def __init__(self):
#         self.fname = 'image.jpg'
#         self.img = Image.open(self.fname)
#         self.point = ()
#
#     def __onclick__(self, click):
#         self.point = (click.xdata, click.ydata)
#         return self.point
#
#     def getCoord(self):
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#         imshow(self.img)
#         #cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
#         plt.show()
#         return self.point
#


class TestClass():

    def __init__(self):
        self.fname = "image"
        self.point = ()
        self.point_list = []
        self.click_left = 1

    def __onclick__(self, click):
        self.point = (click.xdata, click.ydata)
        self.click_left -= 1
        return self.point

    def getCoord(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        imshow(self.img)
        cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
        return self.point

    # def getCoord(self):
    #     self.img = Image.open(self.fname)
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     imshow(self.img)
    #     cid = fig.canvas.mpl_connect(
    #         'button_press_event', self.__onclick__)
    #
    #     fig.canvas.mpl_disconnect(cid)
    #     return self.point

list = []
zero = 1

for image in image_list[1:2]:
    image_name = image.split('/')[-1][0:-4]
    cell_count_GT = int(image_name.split('_')[2].split('C')[1])
    cell_count_GT = 3

    print "Working on:", image_name, "--- %s" % (zero / len(image_list) * 100), '% done'

    click = TestClass()
    click.fname = image
    click.click_left = cell_count_GT
    while click.click_left > len(click.point_list):
        pts = click.getCoord()
        print pts
        click.point_list.append(pts)
        print click.point_list
    else:
        continue
    # print click.getCoord()

    # try:
    #     x, y = zip(*self.point_list)
    #     plt.plot(x, y, 'g^')
