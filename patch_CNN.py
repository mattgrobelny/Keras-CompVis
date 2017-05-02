# from __future__ import print_function
# import keras
# from keras.datasets import cifar10
# from keras.preprocessing.image import ImageDataGenerator
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten
# from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image
import numpy as np
import glob
import cv2

#######
# Directories

# Polar server
#home = '/home/grobeln2/git_files/Keras-CompVis/'

# Mac
home = '/Users/matt/github/Keras-CompVis/'

########
patch_images = '/data/Patches_ALL/'
validation_data_dir = home + 'data/Working_Sets/Validation'
train_data_dir = home + 'data/Working_Sets/Training'
test_data_dir = home + 'data/Working_Sets/Test'
# (x_train, y_train), (x_test, y_test) = cifar10.load_data()
# y_train = np_utils.to_categorical(y_train, num_classes)
# y_test = np_utils.to_categorical(y_test, num_classes)

# string for glob to produce list of files only .jpgs
glob_dir = home + patch_images + '*.jpg'
# print glob_dir

# Get list of images to work on
image_list = glob.glob(glob_dir)
# print image_list


images = []
label = []
img_width = 34
img_height = 34
for image_dir in image_list[1:100]:
    # get image name
    image_name = image_dir.split('/')[-1][0:-4]
    print "Working on:", image_name
    # get image label
    label_val = image_name.split('CX_')[1][0]
    label.append(label_val)

    # open image
    image_open = Image.open(image_dir)

    # reshape to numpy array
    numpy_image = img_to_array(image_open)
    numpy_image = numpy_image.reshape((1,) + numpy_image.shape)
    images.append(numpy_image)
print len(images)


datagen = ImageDataGenerator(
    # featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    horizontal_flip=True,
    channel_shift_range=100)

# compute quantities required for featurewise normalization
# (std, mean, and principal components if ZCA whitening is applied)
datagen.fit(x_train)

# fits the model on batches with real-time data augmentation:
model.fit_generator(datagen.flow(x_train, y_train, batch_size=32),
                    steps_per_epoch=len(x_train) / 32, epochs=epochs)

train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# model.fit_generator(
#     train_generator,
#     steps_per_epoch=nb_train_samples // batch_size,
#     epochs=epochs,
#     validation_data=validation_generator,
#     validation_steps=nb_validation_samples // batch_size)

# model.save_weights('first_try.h5')
#
# # batch_size = 16
# #
# # # this is the augmentation configuration we will use for training
# # train_datagen = ImageDataGenerator(
# #         rescale=1./255,
# #         shear_range=0.2,
# #         zoom_range=0.2,
# #         horizontal_flip=True)
# #
# # # this is the augmentation configuration we will use for testing:
# # # only rescaling
# # test_datagen = ImageDataGenerator(rescale=1./255)
# #
# # # this is a generator that will read pictures found in
# # # subfolers of 'data/train', and indefinitely generate
# # # batches of augmented image data
# # train_generator = train_datagen.flow_from_directory(
# #         'data/train',  # this is the target directory
# #         target_size=(150, 150),  # all images will be resized to 150x150
# #         batch_size=batch_size,
# #         class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels
# #
# # # this is a similar generator, for validation data
# # validation_generator = test_datagen.flow_from_directory(
# #         'data/validation',
# #         target_size=(150, 150),
# #         batch_size=batch_size,
# #         class_mode='binary')
