from __future__ import print_function
import keras
# from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, UpSampling2D, Reshape
from keras.layers import Conv2D, Conv3D, MaxPooling2D, ZeroPadding2D
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
#home = '/Users/matt/github/Keras-CompVis/'

########
# Set up Directories
patch_images = '/data/Patches_ALL/'
validation_data_dir = home + 'data/Working_Sets_Full_Images/Validation/'
train_data_dir = home + 'data/Working_Sets_Full_Images/Training/'
evaulate_data_dir = home + 'data/Working_Sets_Full_Images/Test/'
prediction_data_dir = home + 'data/Working_Sets_Full_Images/Prediction/'
model_dir = home + 'cnn_models/patches_models_Full_Arc_test/'
save_aug_pred_image_dir = home + \
    'data/Working_Sets_Full_Images/Pred_augmented_images/'
prediction_report_images_dir = home + \
    'data/Working_Sets_Full_Images/Prediction/Images_For_Prediction/'
mask_Train_dir = home + 'data/Working_Sets_Full_Images/Masks/Training'
mask_Validation_dir = home + 'data/Working_Sets_Full_Images/Masks/Validation'
mask_evalutaion_dir = home + 'data/Working_Sets_Full_Images/Masks/Test'

# prefix for outfile labels
prefix_out = "full_images_CNN"

# Hyper parameters
batch_size = 10
num_classes = 2
epochs = 5


# Addintial parameters
img_width = 696
img_height = 520

# input_shape=(128, 128, 3) for 128x128 RGB pictures in
# data_format="channels_last".
desired_image_dim = 100  # such that width == height
input_shape_image = (desired_image_dim, desired_image_dim, 3)


# number of training samples
nb_train_samples = 84

# number of training samples
nb_validation_samples = 28

# Weight the empty space more as it is under represented
# class_weight_dic = {'output': {0: 0.75, 1: 0.25}}

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

# print("Starting Data Prep")
# ########################################################
# # Prep training data and mask
# train_generator = datagen.flow_from_directory(
#     train_data_dir,
#     color_mode='rgb',
#     target_size=(desired_image_dim, desired_image_dim),
#     batch_size=batch_size,
#     class_mode=None)
# print("Finished Data Prep: train_generator")
#
# mask_generator_train = datagen.flow_from_directory(
#     mask_Train_dir,
#     class_mode=None,
#     seed=seed)
#
# # combine generators into one which yields image and masks
# train_generator_w_mask = zip(train_generator, mask_generator_train)
#
# ########################################################
# # Prep Validation data and mask
#
# validation_generator = datagen.flow_from_directory(
#     validation_data_dir,
#     color_mode='rgb',
#     target_size=(desired_image_dim, desired_image_dim),
#     batch_size=batch_size,
#     class_mode=None)
#
# mask_generator_validation = datagen.flow_from_directory(
#     mask_Train_dir,
#     class_mode=None,
#     seed=seed)
#
# # combine generators into one which yields image and masks
# validation_generator_w_mask = zip(
#     validation_generator, mask_generator_validation)
# ########################################################

print("Starting Data Prep")
train_generator = datagen.flow_from_directory(
    train_data_dir,
    color_mode='rgb',
    target_size=(desired_image_dim, desired_image_dim),
    batch_size=batch_size,
    class_mode='sparse')
print("Finished Data Prep: train_generator")

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    color_mode='rgb',
    target_size=(desired_image_dim, desired_image_dim),
    batch_size=batch_size,
    class_mode='sparse')
print("Finished Data Prep: validation_generator")


print("Finished Data Prep: validation_generator")

model = Sequential()

# Image detecting  Layers - Start
# 2D Conv 1 (input layer) - None trainable
model.add(Conv2D(1, (3, 3), padding='same',
                 data_format="channels_last",
                 input_shape=input_shape_image,
                 trainable=False))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# 2D Conv 2 - None trainable
model.add(Conv2D(32, (3, 3), trainable=False))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# 2D Conv 3 - None trainable
model.add(Conv2D(64, (3, 3), trainable=False))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 2D Conv 4 - None trainable
model.add(Conv2D(128, (3, 3), trainable=False))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Image detecting  Layers - End

# Layers for patch training recognition
model.add(Flatten())
model.add(Dense(1024))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

# load the weights - From patch training
model.load_weights(model_dir + 'patchcnn_Full_arch.h5')
# print(model.outputs)

# pop last six layers to adjust for heatmap output
model.pop()
model.pop()
model.pop()
model.pop()
model.pop()
model.pop()

print (model.layers[-1])
# model.layers.pop2()
# model.layers.pop2()
# model.layers.pop2()
# model.layers.pop2()
# model.layers.pop2()
# model.layers.pop2()
# https://github.com/fchollet/keras/issues/871
# FC
model.add(Dense(1024))
model.add(Conv2D(512, (3, 3)))
model.add(Activation('relu'))

# UpSampling 1
model.add(UpSampling2D(size=(3, 3)))
model.add(Activation('relu'))
model.add(Conv2D(128, (3, 3)))

# UpSampling 2
model.add(UpSampling2D(size=(3, 3)))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))

# UpSampling 3
model.add(UpSampling2D(size=(3, 3)))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))

# # Final Layer
model.add(Flatten())
model.add(Dense(1, activation="linear", kernel_initializer="uniform"))

print('Finished Building Network Architecture')


# model compile
model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])

print("Saving Model Graphic...")

# # Save image of model /// pip install pydot-ng or pydot as sudo?
plot_model(model, to_file=model_dir + prefix_out + '.png', show_shapes=True)
print("Model graphic Saved")
print("Starting Training")
model_fit = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    # class_weight=class_weight_dic
)

# print(model_fit.history)
print("Finished Training")

print("Saving Model...")

model.save_weights(model_dir + prefix_out + '.h5')
print("Model Saved")

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
plt.savefig(model_dir + prefix_out + "_Metric.jpg",
            dpi=200, rasterized=True)
plt.close()
print("Plot Saved as:")
print(model_dir + prefix_out + "_Metric.jpg")
print("DONE!")


##############################################################################
# Model evaulation and predition code
steps_eval = 10

print("Starting model evalution and predition test")

# Model evaluate data generator
evalution_generator = datagen.flow_from_directory(
    evaulate_data_dir,
    color_mode='rgb',
    target_size=(desired_image_dim, desired_image_dim),
    batch_size=batch_size,
    class_mode='sparse')

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
    target_size=(desired_image_dim, desired_image_dim),
    batch_size=1,
    shuffle=False,
    save_prefix="aug_",
    class_mode='sparse',
    save_to_dir=save_aug_pred_image_dir)

print("Finished Data Prep: prediction_generator")

print("running model prediction test...")
print("prediction data dir: " + prediction_data_dir)
model_predict = model.predict_generator(
    prediction_generator,
    steps=10,
    max_q_size=1,
    pickle_safe=True)
print(model_predict)

##################################################
# Prep Image Predition Report CSV
report_fh = open(prediction_report_images_dir +
                 prefix_out + "_Report.csv", 'w')
image_list = glob.glob(prediction_report_images_dir + '*.jpg')

# print(image_list)

print("Saveing Prediction Report...")
report_fh.write("Image Dir,Image_name,GroundTruth, P_None_Nuc, P_Nuclei \n")
for i in range(len(model_predict)):
    image_name = image_list[i].split('/')[-1][0:-4]
    image_cat = image_name.split('_')[-1]
    report_fh.write("%s,%s,%s,%s,%s \n" % (image_list[i], image_name, image_cat,
                                           model_predict[i][0], model_predict[i][1]))
print("Done!")
report_fh.close()

##################################################
# Prep Image Predition Report Markdown
report_fh = open(prediction_report_images_dir +
                 prefix_out + "_Report.md", 'w')
image_list = glob.glob(prediction_report_images_dir + '*.jpg')

# print(image_list)

print("Saveing Prediction Report...")
report_fh.write("|Image|Image_name|GroundTruth| P_None_Nuc| P_Nuclei| \n")
report_fh.write(
    '| :------------- | :------------- |:------------- |:------------- |:------------- | \n')
for i in range(len(model_predict)):
    image_name = image_list[i].split('/')[-1][0:-4]
    image_cat = image_name.split('_')[-1]
    report_fh.write("|![image](%s)|%s|%s|%s|%s| \n" % (image_list[i].split('/')[-1][0:-4], image_name, image_cat,
                                                       model_predict[i][0], model_predict[i][1]))
print("Done!")
report_fh.close()
