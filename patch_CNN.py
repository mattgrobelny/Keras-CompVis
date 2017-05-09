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
# import pydot
# import glob
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob


#######
# Directories

# Polar server
home = '/home/grobeln2/git_files/Keras-CompVis/'

# Mac
# home = '/Users/matt/github/Keras-CompVis/'

########
# Set up Directories
patch_images = '/data/Patches_ALL/'
validation_data_dir = home + 'data/Working_Sets_Patches/Validation/'
train_data_dir = home + 'data/Working_Sets_Patches/Training/'
evaulate_data_dir = home + 'data/Working_Sets_Patches/Test/'
prediction_data_dir = home + 'data/Working_Sets_Patches/Prediction/'
model_dir = home + 'cnn_models/patches_models/'
save_aug_pred_image_dir = home + 'data/Working_Sets_Patches/Pred_augmented_images/'

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

# Weight the empty space more as it is under represented
class_weight_dic = {'output': {0: 0.75, 1: 0.25}}

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
model_fit = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    class_weight=class_weight_dic)
# print(model_fit.history)
print("Finished Training")

print("Saving Model...")

model.save_weights(model_dir + 'first_try.h5')

print("Model Saved")

print("Saving Model Graphic...")

# # Save image of model /// pip install pydot-ng or pydot as sudo?
plot_model(model, to_file=model_dir + 'patch_CNN_model.png', show_shapes=True)
print("Model graphic Saved")
##############################################################################
# Plot metrics

print("Plotting Metrics")
# Set up x range
x = range(1, epochs + 1)

# start plot
fig, ax1 = plt.subplots()

# Plot Accuracy
ax1.plot(x, model_fit.history['acc'], linewidth=2,
         label='Train Accuracy', color='blue')

ax1.plot(x, model_fit.history['val_acc'],
         label='Val Accuracy', color='red')
ax1.set_ylabel('Accuracy (%)')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_xlabel('Epochs #')
ax1.tick_params('y')
ax1.set_ylim([0, 1])

plt.legend(loc='right')

# Plot Loss

ax2 = ax1.twinx()

ax2.plot(x, model_fit.history['loss'], label='Train', color='blue')

ax2.plot(x, model_fit.history['val_loss'],
         label='Validation', linewidth=2, color='red', linestyle='--')
ax2.set_ylabel('Loss Metric', color='r')
ax2.tick_params('y')

# second axis limits
combine_loss = []
combine_loss.append(model_fit.history['val_loss'])
combine_loss.append(model_fit.history['loss'])
ax2.set_ylim([0, max(max(combine_loss))])

# adjust x axis
plt.legend(loc='right')
plt.xlim(1, epochs)
plt.xticks(x)

# save fig
plt.savefig(model_dir + "Metric_Patch_CNN.jpg", dpi=200, rasterized=True)
plt.close()
print("Plot Saved as:")
print(model_dir + "Metric_Patch_CNN.jpg")
print("DONE!")


##############################################################################
# Model evaulation and predition code
steps_eval = 10

print("Starting model evalution and predition test")

# Model evaluate data generator
evalution_generator = datagen.flow_from_directory(
    evaulate_data_dir,
    color_mode='rgb',
    target_size=(35, 35),
    batch_size=batch_size,
    class_mode='categorical')

print("Finished Data Prep: evalution_generator")

print("running model evaluation...")
# Model evaluate function
model_eval = model.evaluate_generator(evalution_generator, steps_eval, max_q_size=10,
                                      workers=10, pickle_safe=False)

print("# --- Model evaluation Results --- #")
for i in range(len(model.metrics_names)):
    print(model.metrics_names[i], ' --- ', model_eval[i])

##################################################
# Run prediction test on a subset of images (10)
print("")
print("Running model prediction test..")

prediction_generator = datagen.flow_from_directory(
    prediction_data_dir,
    color_mode='rgb',
    target_size=(35, 35),
    batch_size=1,
    shuffle=False,
    save_prefix="aug_",
    save_to_dir=save_aug_pred_image_dir)

print("Finished Data Prep: prediction_generator")

print("running model prediction test...")
print("prediction data dir: " + prediction_data_dir)
model_predict = model.predict_generator(
    prediction_generator,
    steps=10,
    max_q_size=1,
    pickle_safe=False)
print(model_predict)

report_fh = open(save_aug_pred_image_dir + "prediction_report", 'w')
# # Prep Image Predition Report
# image_list = glob.glob(save_aug_pred_image_dir + "*.jpg)
# print("# --- Model evaluation Results --- #")
# for i in range(len(model_predict)):
#     print(model.metrics_names[i], ' --- ', model_eval[i])
