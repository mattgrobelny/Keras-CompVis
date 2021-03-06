# Understanding Keras - Key Parameters

What does "sample", "batch", "epoch" mean?

Below are some common definitions that are necessary to know and understand to correctly utilize Keras:

- Sample: one element of a dataset.  
Example: one image is a sample in a convolutional network  
Example: one audio file is a sample for a speech recognition model  

- Batch: a set of N samples. The samples in a batch are processed independently, in parallel. If training, a batch results in only one update to the model.  
A batch generally approximates the distribution of the input data better than a single input. The larger the batch, the better the approximation; however, it is also true that the batch will take longer to processes and will still result in only one update. For inference (evaluate/predict), it is recommended to pick a batch size that is as large as you can afford without going out of memory (since larger batches will usually result in faster evaluating/prediction).

- Epoch: an arbitrary cutoff, generally defined as "one pass over the entire dataset",
used to separate training into distinct phases, which is useful for logging and periodic evaluation.
When using evaluation_data or evaluation_split with the fit method of Keras models, evaluation will be run at the end of every epoch.  
Within Keras, there is the ability to add callbacks specifically designed to be run at the end of an epoch.
Examples of these are learning rate changes and model checkpointing (saving).  

# Understanding Kera - Training output
171/171 [==============================] - 72s - loss: 11.5645 - acc: 0.2805 - val_loss: 11.8235 - val_acc: 0.2664
Epoch 2/2
