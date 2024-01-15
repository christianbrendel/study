import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import time


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28*28, 5000)
        self.fc2 = nn.Linear(5000, 3000)
        self.fc3 = nn.Linear(3000, 10)


    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        return x


def train(device, epochs=1):

    net = Net()
    net.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    
    net.train()

    start_time = time.time()
    for epoch in range(epochs):  
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data[0].to(device), data[1].to(device)

            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 100 == 99:
                print(f"[{epoch + 1}, {i + 1}] loss: {running_loss / 100:.3f}", end='\r')
                running_loss = 0.0
    
    d = device.type.upper()
    dt = time.time() - start_time
    print(f'Finished Training on {d}: Training time = {dt:.3f} seconds')

if __name__ == '__main__':

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

    train(torch.device('mps'), epochs=1)
    train(torch.device('cpu'), epochs=1)
    