from __future__ import print_function
import keras
# from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import plot_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image
import numpy as np
import h5py
import graphviz
import pydot
import glob
import cv2

#######
# Directories

# Polar server
home = '/home/grobeln2/git_files/Keras-CompVis/'

# Mac
#home = '/Users/matt/github/Keras-CompVis/'

########
patch_images = '/data/Patches_ALL/'
validation_data_dir = home + 'data/Working_Sets_Patches/Validation/'
train_data_dir = home + 'data/Working_Sets_Patches/Training/'
test_data_dir = home + 'data/Working_Sets_Patches/Test/'
model_dir = home + 'cnn_models/patches_models/'
# (x_train, y_train), (x_test, y_test) = cifar10.load_data()
# y_train = np_utils.to_categorical(y_train, num_classes)
# y_test = np_utils.to_categorical(y_test, num_classes)

# # string for glob to produce list of files only .jpgs
# glob_dir = home + patch_images + '*.jpg'
# # print glob_dir
#
# # Get list of images to work on
# image_list = glob.glob(glob_dir)
# # print image_list


# images = []
# label = []

# Hyper parameters
batch_size = 30
num_classes = 2
epochs = 1

# Addintial parameters
img_width = 35
img_height = 35

# input_shape=(128, 128, 3) for 128x128 RGB pictures in
# data_format="channels_last".
input_shape_image = (35, 35, 3)

# number of training samples
nb_train_samples = 5475

# number of training samples
nb_validation_samples = 1826

print('Stating patch CNN')

datagen = ImageDataGenerator(
    # featurewise_center=True,
    # featurewise_std_normalization=True,
    # rotation_range=20,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    channel_shift_range=100)

# compute quantities required for featurewise normalization
# (std, mean, and principal components if ZCA whitening is applied)
# datagen.fit(x_train)
#
# # fits the model on batches with real-time data augmentation:
# model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),
#                     steps_per_epoch=len(x_train) / batch_size, epochs=epochs)
print("Starting Data Prep")
train_generator = datagen.flow_from_directory(
    train_data_dir,
    color_mode='rgb',
    target_size=(35, 35),
    batch_size=batch_size,
    class_mode='categorical')
print("Finished Data Prep: train_generator")

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    color_mode='rgb',
    target_size=(35, 35),
    batch_size=batch_size,
    class_mode='categorical')
print("Finished Data Prep: validation_generator")

model = Sequential()

model.add(Conv2D(35, (3, 3), padding='same',
                 data_format="channels_last",
                 input_shape=input_shape_image))
model.add(Activation('relu'))
model.add(Conv2D(35, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(70, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(70, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(560))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

print('Finished Building Network Architecture')

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

print("Starting Training")
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

print("Finished Training")

print("Saving Model...")

model.save_weights(model_dir + 'first_try.h5')

print("Model Saved")

# Save image of model
plot_model(model, to_file=home + 'patch_CNN_model.png', show_shapes=True)
