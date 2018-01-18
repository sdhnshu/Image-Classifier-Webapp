from base64 import b64decode
from PIL import Image
from io import BytesIO
from torchvision import models, transforms
from torch.autograd import Variable
import torch.nn as nn
import numpy as np
import pickle


def process_image(image):
    print('process!!!')

    image = Image.open(BytesIO(b64decode(image)))
    print('image', image)
    trans = transforms.Compose([
        transforms.Resize(224),
        transforms.RandomCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    image = Variable(trans(image))
    print(image)
    image = image.view(1, 3, 224, 224)
    print('loading model')
    model = models.resnet18(pretrained=True, num_classes=1000).eval()
    print('model loaded')

    softmax = nn.LogSoftmax(1)
    preds = softmax(model(image)).data.cpu().numpy()
    print(preds)
    res = np.argmax(preds)
    print(res)

    with open('classes.pkl', 'rb') as f:
        imagenet_classes = pickle.load(f)
        print(imagenet_classes)
    print(imagenet_classes[res].split(',')[0])

    return imagenet_classes[res].split(',')[0]
