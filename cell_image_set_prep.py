from PIL import Image

# Dir for images
image_location = '/home/mgrobelny/Data/IB271/IB271_jpg/lab5/'
jpg = '*.jpg'

# string for glob to produce list of files only .jpgs
glob_dir = image_location + jpg
# print glob_dir

image_list = glob.glob(image_location + jpg)

# output location
image_location_output = '/home/mgrobelny/Data/IB271/IB271_jpg/lab5/Dominate_colors_cluster_9/'

for image in image_list:
    im = Image.open(image)
    image_name = image.split('/')[-1][0:-4]
    print "Working on:", image_name, "--- %s" % (zero / len(image_list) * 100), '% done'
    image_data = cv2.imread(image)
    image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

    # reshape the image to be a list of pixels
    image_data = image_data.reshape(
        (image_data.shape[0] * image_data.shape[1], 3))

    plt.imshow(bar)
    plt.savefig(image_location_output + "%s_Dominate_colors.png" %
                (image_name), dpi=500)
    plt.close()
