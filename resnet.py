import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import transforms, datasets, models
from tqdm import tqdm
import matplotlib.pyplot as plt

model = models.resnet18(pretrained=False)

in_features = model.fc.in_features
model.fc = nn.Linear(in_features, 11)

data_dir = 'dataset'

def load_train(datadir):
    train_transforms = transforms.Compose([transforms.Resize(256),
                                       transforms.ToTensor(),
                                       ])
    trainset = datasets.ImageFolder(datadir,       
                    transform=train_transforms)
    
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=16,
                                              shuffle=True)
    return trainset, trainloader

trainset, trainloader = load_train(data_dir)
print(trainloader.dataset.classes)

#trainset = datasets.CIFAR10(root = './data', train = True, download = True, transform = transforms.Compose([transforms.ToTensor(), 
#                                                                             transforms.Normalize((0.5, 0.5, 0.5),
#                                                                                                  (0.5, 0.5, 0.5))]))

#trainloader = torch.utils.data.DataLoader(trainset, batch_size=16,
#                                          shuffle=True)
#accloader = torch.utils.data.DataLoader(trainset, batch_size=16, shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.003)

epoch_losses = []
epoch_accs = []

for i in range(5):
    epoch_loss = 0.0
    epoch_acc = 0
    
    for data, labels in tqdm(trainloader):
        
        outputs = model(data)
        
        loss = criterion(outputs, labels)
            
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        with torch.no_grad():
            for i, elem in enumerate(torch.argmax(outputs, 1)):
                if elem == labels[i]:
                    epoch_acc += 1
        epoch_loss += loss.item()
    
    print("")
    print("Loss: " + str(epoch_loss / len(trainloader)))
    epoch_losses.append(epoch_loss / len(trainloader))
    print("Accuracy: " + str(epoch_acc / len(trainset)) + "%")
    epoch_accs.append(epoch_acc / len(trainset))
    
    torch.save(model.state_dict(), 'torch_model/resnet18.pth')
        
plt.plot(epoch_losses)
plt.plot(epoch_accs)
