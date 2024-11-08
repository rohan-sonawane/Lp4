#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Implementing Feed-forward neural networks with Keras and TensorFlow 
a. Import the necessary packages 
b. Load the training and testing data (MNIST/CIFAR10) 
c. Define the network architecture using Keras 
d. Train the model using SGD 
e. Evaluate the network 
f. Plot the training loss and accuracy '''
# a. Import the necessary packages -->
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import random
# b. Load the training and testing data (MNIST/CIFAR10) -->
mnist = tf.keras.datasets.mnist                          #Importing MNIST dataset
# Splitting it into training and testing data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train / 255
x_test = x_test / 255
# c. Define the network architecture using Keras   -->
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10,activation="softmax")
])

model.summary()
# d. Train the model using SGD  -->
model.compile(optimizer="sgd",
loss="sparse_categorical_crossentropy",
metrics=['accuracy'])

history=model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=3)
# e. Evaluate the network   -->
test_loss,test_acc=model.evaluate(x_test,y_test)
print("Loss=%.3f" %test_loss)
print("Accuracy=%.3f" %test_acc)

n=random.randint(0,9999)
plt.imshow(x_test[n])
plt.show()
predicted_value=model.predict(x_test)
plt.imshow(x_test[n])
plt.show()

print('Predicted value: ', predicted_value[n])
# f. Plot the training loss and accuracy  -->

#Plotting the training accuracy

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()


# In[ ]:


'''
Build the Image classification model by dividing the model into the following four stages: 
a. Loading and preprocessing the image data 
b. Defining the model’s architecture 
c. Training the model 
d. Estimating the model’s performance'''
# Importing required packages
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense,Conv2D, Dropout, Flatten, MaxPooling2D
import matplotlib.pyplot as plt
import numpy as np
# a. Loading and preprocessing the image data

mnist=tf.keras.datasets.mnist
# Splitting into training and testing data
(x_train,y_train),(x_test,y_test) = mnist.load_data()
input_shape = (28,28,1)
# Making sure that the values are float so that we can getdecimal points after division
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
# print("Data type of x_train:", x_train.dtype)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
# print("Data type after converting to float:", x_train.dtype)
# Normalizing the RGB codes by divinding it into the max RGB value.
x_train = x_train / 255
x_test = x_test / 255
print("Shape of training : ", x_train.shape)
print("Shape of testing : ", x_test.shape)
# b. Defining the model’s architecture
model = Sequential()
model.add(Conv2D(28, kernel_size=(3,3), input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(200,activation = "relu"))
model.add(Dropout(0.3))

model.add(Dense(10,activation = "softmax"))
model.summary()
# c. Training the model
model.compile(optimizer="adam",
loss="sparse_categorical_crossentropy",metrics=['accuracy'])
model.fit(x_train,y_train,epochs=2)
# d. Estimating the model’s performance
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Loss=%.3f" %test_loss)
print("Accuracy=%.3f" %test_acc)
# Showing image at positions[] from dataset: 
image = x_train[5]
plt.imshow(np.squeeze(image), cmap='gray')
plt.show()
# Predicting the class of image :
image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])
predict_model = model.predict([image])
print("Predicted class {}:" .format(np.argmax(predict_model)))


# In[ ]:


'''
Implement the Continuous Bag of Words (CBOW) Model. Stages can be: 
a. Data preparation 
b. Generate training data 
c. Train model 
d. Output '''
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import matplotlib.pylab as pylab
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import re
sentences = """We are about to study the idea of a computational process.
Computational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells."""
#Clean Data
# remove special characters
sentences = re.sub('[^A-Za-z0-9]+', ' ', sentences)

# remove 1 letter words
sentences = re.sub(r'(?:^| )\w(?:$| )', ' ', sentences).strip()

# lower all characters
sentences = sentences.lower()
#Vocabulary
words = sentences.split()
vocab = set(words)
vocab_size = len(vocab)
embed_dim = 10
context_size = 2
#Implementation
word_to_ix = {word: i for i, word in enumerate(vocab)}
ix_to_word = {i: word for i, word in enumerate(vocab)}
#Data bags
# data - [(context), target]

data = []
for i in range(2, len(words) - 2):
    context = [words[i - 2], words[i - 1], words[i + 1], words[i + 2]]
    target = words[i]
    data.append((context, target))
print(data[:5])
#Embeddings
embeddings =  np.random.random_sample((vocab_size, embed_dim))
#Linear Model
def linear(m, theta):
    w = theta
    return m.dot(w)
#Log softmax + NLLloss = Cross Entropy
def log_softmax(x):
    e_x = np.exp(x - np.max(x))
    return np.log(e_x / e_x.sum())
def NLLLoss(logs, targets):
    out = logs[range(len(targets)), targets]
    return -out.sum()/len(out)
def log_softmax_crossentropy_with_logits(logits,target):

    out = np.zeros_like(logits)
    out[np.arange(len(logits)),target] = 1

    softmax = np.exp(logits) / np.exp(logits).sum(axis=-1,keepdims=True)

    return (- out + softmax) / logits.shape[0]
#Forward function
def forward(context_idxs, theta):
    m = embeddings[context_idxs].reshape(1, -1)
    n = linear(m, theta)
    o = log_softmax(n)

    return m, n, o
#Backward function
def backward(preds, theta, target_idxs):
    m, n, o = preds

    dlog = log_softmax_crossentropy_with_logits(n, target_idxs)
    dw = m.T.dot(dlog)

    return dw
#Optimize function
def optimize(theta, grad, lr=0.03):
    theta -= grad * lr
    return theta
#Training
theta = np.random.uniform(-1, 1, (2 * context_size * embed_dim, vocab_size))

epoch_losses = {}

for epoch in range(80):

    losses =  []

    for context, target in data:
        context_idxs = np.array([word_to_ix[w] for w in context])
        preds = forward(context_idxs, theta)

        target_idxs = np.array([word_to_ix[target]])
        loss = NLLLoss(preds[-1], target_idxs)

        losses.append(loss)

        grad = backward(preds, theta, target_idxs)
        theta = optimize(theta, grad, lr=0.03)


    epoch_losses[epoch] = losses
#Analyze
#Plot loss/epoch
ix = np.arange(0,80)

fig = plt.figure()
fig.suptitle('Epoch/Losses', fontsize=20)
plt.plot(ix,[epoch_losses[i][0] for i in ix])
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Losses', fontsize=12)
#Predict function
def predict(words):
    context_idxs = np.array([word_to_ix[w] for w in words])
    preds = forward(context_idxs, theta)
    word = ix_to_word[np.argmax(preds[-1])]

    return word
# (['we', 'are', 'to', 'study'], 'about')
a=predict(['we', 'are', 'to', 'study'])
print(a)
#Accuracy
def accuracy():
    wrong = 0

    for context, target in data:
        if(predict(context) != target):
            wrong += 1

    return (1 - (wrong / len(data)))

accuracy()
predict(['processes', 'manipulate', 'things', 'study'])

