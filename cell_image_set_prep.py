from PIL import Image
import glob
import cv2
import matplotlib.pyplot as plt


# Dir for images
image_location = '/Users/matt/github/Keras-CompVis/data/one_cell/'
jpg = '*.TIF'

# string for glob to produce list of files only .jpgs
glob_dir = image_location + jpg
# print glob_dir

# Get list of images to work on
image_list = glob.glob(image_location + jpg)
print image_list

# output location
image_location_output = '/Users/matt/github/Keras-CompVis/data/one_cell_patches'


zero = 1
for image in image_list[1:2]:
    im = Image.open(image)
    image_name = image.split('/')[-1][0:-4]
    print "Working on:", image_name, "--- %s" % (zero / len(image_list) * 100), '% done'

    # Load greyscale version
    image_data_grey = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    # find threshold
    (thresh, im_bw) = cv2.threshold(image_data_grey,
                                    128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    im_bw = cv2.threshold(image_data_grey, thresh, 255, cv2.THRESH_BINARY)

    print im_bw
    Image.fromstring(mode, size, im_bw)

    im = Image.new("RGB", (50, 50), "black")

    # # reshape the image to be a list of pixels
    # image_data = image_data.reshape(
    #     (image_data.shape[0] * image_data.shape[1], 3))
    #
    # plt.imshow(bar)
    # plt.savefig(image_location_output + "%s_Dominate_colors.png" %
    #             (image_name), dpi=500)
    # plt.close()
