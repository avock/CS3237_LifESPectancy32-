import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

import cv2
from opencv import segment_hand

class CNNModel(nn.Module):
    def __init__(self): # class constructor function

        super(CNNModel, self).__init__() # initialize an instance of the parent class

        # first convolutional and maxpool layer
        # input 1x120x100, output 16x116x96
        self.conv1 = nn.Conv2d(in_channels = 1, out_channels = 16, kernel_size=(5, 5))
        # input 16x116x96, output 16x58x48
        self.maxpool1 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        # second convolutional and maxpool layer
        # input 16x58x48, output 32x54x44
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(5, 5))
        # input 32x54x44, output 32x27x22
        self.maxpool2 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        # linear layer
        self.fc1 = nn.Linear(in_features=19008, out_features=120)
        self.fc2 = nn.Linear(120,84)
        self.fc3 = nn.Linear(84,6)


    def forward(self, x):
        # Layer 1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.maxpool1(x)

        # Layer 2
        x = self.conv2(x)
        x = F.relu(x)
        x = self.maxpool2(x)

        # Output Fully Connected Layers
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        output = x

        # return the output predictions
        return output

model = CNNModel()
model.load_state_dict(torch.load("/root/src/ML/model/handclassifier.pt",map_location=torch.device('cpu')))


bg = cv2.imread('/root/static/bg1.jpg')
target_img = cv2.imread('/root/static/hand1.jpg')

gray_img = segment_hand(bg, target_img)
img_tensor_x = torch.Tensor(gray_img)

# with torch.no_grad():
  
#   output = model(img_tensor_x)
#   print(output)

#   _, pred = torch.max(output, 1)
#   print(pred)
