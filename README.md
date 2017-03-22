# Keras-CompVis
Stats530 Computer vision project

## Goals:
Train a CNN to count cells from microscope images. 

### There are several things I think we should determine:
1. Exactly what do we want to count/identify from an image.
2. Determine what data would be easiest to use.
3. Which package/s should we use to start figuring out how to approach this problem.
    Something like this: http://scikit-learn.org/stable/  

### Challenges :
1. Figuring how to properly label the data
2. Labeling the data
3. Optimizing the machine learning algorithm for our specific problem.

### CNN vs NN :
- http://stats.stackexchange.com/questions/114385/what-is-the-difference-between-convolutional-neural-networks-restricted-boltzma
- [CS231n Convolutional Neural Networks for Visual Recognition](http://cs231n.github.io/convolutional-networks/)

### List of functionalities we will need:
- [ ] Data Labeler : Display images--> allows user to count number of cells and added it to the image meta data/table. (generate labeled data to train model)
- [ ] Model Trainer - train model on half of our data
- [ ] Model Test - test model on the other half of our data
- [ ] Application - Input image --> outputs cell count (only if model has a high accuracy)

### Data  
Need to find a source for images which have features which can be easily identified
1. https://data.broadinstitute.org/bbbc/image_sets.html
2. http://www.cs.tut.fi/sgn/csb/simcep/benchmark/ (Benchmark images)

From: https://www.tensorflow.org/tutorials/deep_cnn
For training, we additionally apply a series of random distortions to artificially increase the data set size:
- Randomly flip the image from left to right.
- Randomly distort the image brightness.
- Randomly distort the image contrast.

### Libraries:
- Keras (https://github.com/fchollet/keras)
- Tensorflow (https://www.tensorflow.org)
- OpenCV (http://opencv.org)
- Scikit-learn (http://scikit-learn.org/stable/)

### Keras guides
https://keras.io/getting-started/sequential-model-guide/

### Tensor Flow guides:
- [A Guide to TF Layers: Building a Convolutional Neural Network](https://www.tensorflow.org/tutorials/layers)

Small images training
https://github.com/fchollet/keras/blob/master/examples/cifar10_cnn.py
