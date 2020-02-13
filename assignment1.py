# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14q_9z0DC6h5jWrFtqNvQLs74FC0hly11

### **Assignment 1**
Nonlinear Regression using Deep Convolutional Neural network
"""

# Pandas library: To read the dataset
import pandas as pd
# Read the dataset 'housing.csv'
dataset = pd.read_csv('/content/housing.csv')
# Print first 10 records with the help head(n) function
tenRecords = dataset.head(10)
print('The first 10 records of the dataset:')
tenRecords

"""Plotting of dataset features for first 40 samples."""

import matplotlib.pyplot as plt
columns = dataset.columns.drop(['ocean_proximity'])
datasetSampleForGraph = dataset.head(40)
fig, ax = plt.subplots(nrows=9, ncols=1)
x_data = range(0,datasetSampleForGraph.shape[0])
i=0
# Plot the feature subplots for given housing dataset
# Each feature will be having a seperate subplot
print('                     Housing Dataset')
for column in columns:
  ax[i].plot(x_data, datasetSampleForGraph[column], label=column)
  ax[i].legend()
  i = i + 1

"""Nonlinear regression model"""

#Remove any incomplete entries
dataset=dataset.dropna()

#We will predict the "median_house_value" column
Y = dataset['median_house_value']

X=dataset.loc[:,'longitude':'median_income']

#Split the dataset into 70:30 ratio
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.3)

#Converts the datasets to numpy arrays to work with PyTorch model
x_train_np=x_train.to_numpy()
y_train_np=y_train.to_numpy()
#Convert the testing data
x_test_np=x_test.to_numpy()
y_test_np=y_test.to_numpy()

import torch
#1D convolutional layer, we are inputting 1-dimensional row of data.
from torch.nn import Conv1d
#max pooling layer
from torch.nn import MaxPool1d
from torch.nn import Flatten
from torch.nn import Linear
from torch.nn.functional import relu
from torch.nn import BatchNorm1d

#dataloader is for taking the dataset from tensordataset and input it in minibatchsizes
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import Adam
from torch.nn import L1Loss

!pip install pytorch-ignite
from ignite.contrib.metrics.regression.r2_score import R2Score

#define the model
class CnnRegressor(torch.nn.Module):

  def __init__(self, batch_size, inputs, outputs):
    super(CnnRegressor, self).__init__()
    self.batch_size = batch_size
    self.inputs = inputs
    self.outputs = outputs
    #Convolutional block consists of convolutional layer, Max pooling layer,
    #Batch_Normalization layer

    #Define the input layer - 1st convolutional layer
    self.input_layer = Conv1d(inputs, batch_size, 1)
    self.batchNorm = BatchNorm1d(batch_size)
    self.max_pooling_layer = MaxPool1d(1)

    #Define 2nd convolutional block
    self.conv_layer = Conv1d(batch_size, 128, 1)
    self.batchNorm1 = BatchNorm1d(128)
    self.max_pooling_layer1 = MaxPool1d(1)
    #Define 3rd convolutional block
    self.conv_layer1 = Conv1d(128, 128, 1)
    self.batchNorm2 = BatchNorm1d(128)
    self.max_pooling_layer2 = MaxPool1d(1)
    #Define 4th convolutional block
    self.conv_layer2 = Conv1d(128, 128, 1)
    self.batchNorm3 = BatchNorm1d(128)
    self.max_pooling_layer3 = MaxPool1d(1)
    #Define 5th convolutional block
    self.conv_layer3 = Conv1d(128, 128, 1)
    self.batchNorm4 = BatchNorm1d(128)
    self.max_pooling_layer4 = MaxPool1d(1)
    #Define 6th convolutional block
    self.conv_layer4 = Conv1d(128, 128, 1)
    self.batchNorm5 = BatchNorm1d(128)
    self.max_pooling_layer5 = MaxPool1d(1)

    #it becomes single FC regular NN after flattening
    self.flatten_layer = Flatten()

    #First linear layer
    #input channels = 128, output  = 64
    self.linear_layer1 = Linear(128,64)
    #second linear layer
    self.linear_layer2 = Linear(64,32)
    #Third linear layer
    self.linear_layer3 = Linear(32,32)
    #Output layer with 1real value as an output
    self.output_layer = Linear(32, outputs)

  # A method to feed inputs through the model
  def feed(self, input):
    #Reshape is converting the 2D inputs to 3D model as it expects
    #3D array to prcoess in 1D fashion
    input = input.reshape((self.batch_size, self.inputs, 1))
    output = self.input_layer(input)
    output = relu(self.batchNorm(output))

    output = self.max_pooling_layer(output)

    #Relu as an activation layer to get a nonlinear regression model
    output = self.max_pooling_layer1(relu(self.batchNorm1(self.conv_layer(output))))
    output = self.max_pooling_layer2(relu(self.batchNorm2(self.conv_layer1(output))))
    output = self.max_pooling_layer3(relu(self.batchNorm3(self.conv_layer2(output))))
    output = self.max_pooling_layer4(relu(self.batchNorm4(self.conv_layer3(output))))
    output = self.max_pooling_layer5(relu(self.batchNorm5(self.conv_layer4(output))))

    output = self.flatten_layer(output)

    output = self.linear_layer1(output)
    output = self.linear_layer2(output)
    output = self.linear_layer3(output)
    
    output = self.output_layer(output)
    return output

#Define the model
batch_size = 128
#Batch size, inputs and outputs
model = CnnRegressor(batch_size, X.shape[1], 1)
model.cuda()

# This method will return the average L1 loss and R2 score
def model_loss(model, dataset, train = False, optimizer = None):
  #Cycle through the batches and get avg L1 loss
  performance = L1Loss()
  score_metric = R2Score()

  avg_loss = 0
  avg_score = 0
  count = 0
  for input, output in iter(dataset):
    #Model's predictoins for the training dataset
    predictions = model.feed(input)

    #Model's loss
    loss = performance(predictions, output)

    #Get the model's R2 score
    score_metric.update([predictions, output])
    score = score_metric.compute()

    if(train):
      #clear errors so that they dont accumulate
      optimizer.zero_grad()
      #compute gradients for our optimizer
      loss.backward()
      #use optimizer to update the model's parameters based on the gradients
      optimizer.step()

    #store the loss and update the counter
    avg_loss += loss.item()
    avg_score += score
    count += 1
  return avg_loss / count, avg_score / count

from time import time
start_time = time()
#Train the model
epochs = 300
#Use Adam as an optimization algorithm instead of SGD for fast convergence
#Adam always outperforms SGD in CNN
optimizer = Adam(model.parameters(), lr=0.001)
inputs = torch.from_numpy(x_train_np).cuda().float()
outputs = torch.from_numpy(y_train_np.reshape(y_train_np.shape[0], 1)).cuda().float()

#Create a dataloader instance to work with our batches
tensor = TensorDataset(inputs, outputs)
loader = DataLoader(tensor, batch_size, shuffle=True, drop_last=True)

for epoch in range(epochs):
  avg_loss, avg_r2_score = model_loss(model, loader, train=True, optimizer=optimizer)

  print("Epoch " + str(epoch+1) + ":\n\tLoss = " + str(avg_loss) + "\n\tR^2 Score = " + str(avg_r2_score))
#### Time taken for training the model
time_taken = time() - start_time
print("Inference time: %.4f s" % time_taken)

#Test the testing dataset using trained model
inputs = torch.from_numpy(x_test_np).cuda().float()
outputs = torch.from_numpy(y_test_np.reshape(y_test_np.shape[0], 1)).cuda().float()

#Create a dataloader instance to work with our batches
tensor = TensorDataset(inputs, outputs)
loader = DataLoader(tensor, batch_size, shuffle=True, drop_last=True)

avg_loss, avg_r2_score = model_loss(model, loader)
print("The model's L1loss is:" + str(avg_loss))
print("The model's R^2score is:" + str(avg_r2_score))

# Save the model in a file
modelSaved = {'model': CnnRegressor(128,8,1),
          'state_dict': model.state_dict(),
          'optimizer' : optimizer.state_dict()}
torch.save(modelSaved, '1095709_1dconv_reg')