import torch
import torch.nn as nn
import cv2
import os
import numpy as np
import math
from PIL import Image
from torchvision import transforms
from django.core.files.base import ContentFile
from .models import Thumbnail, Video
from django.utils import timezone

# Set the device to CPU
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

device = torch.device("cpu")

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()

        def conv_block(in_channels, out_channels, kernel_size=3, padding=1, stride=1):
            return nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True)
            )

        def deconv_block(in_channels, out_channels, kernel_size=2, stride=2):
            return nn.Sequential(
                nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True)
            )

        self.encoder1 = nn.Sequential(conv_block(3, 64), nn.MaxPool2d(2))
        self.encoder2 = nn.Sequential(conv_block(64, 128), nn.MaxPool2d(2))
        self.encoder3 = nn.Sequential(conv_block(128, 256), nn.MaxPool2d(2))
        self.encoder4 = nn.Sequential(conv_block(256, 512), nn.MaxPool2d(2))

        self.decoder1 = deconv_block(512, 256)
        self.decoder2 = deconv_block(512, 128)
        self.decoder3 = deconv_block(256, 64)
        self.decoder4 = deconv_block(128, 64)

        self.final_conv = nn.Conv2d(64, 3, kernel_size=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        enc1 = self.encoder1(x)
        enc2 = self.encoder2(enc1)
        enc3 = self.encoder3(enc2)
        enc4 = self.encoder4(enc3)

        dec1 = self.decoder1(enc4)
        dec1 = torch.cat((enc3, dec1), dim=1)
        dec2 = self.decoder2(dec1)
        dec2 = torch.cat((enc2, dec2), dim=1)
        dec3 = self.decoder3(dec2)
        dec3 = torch.cat((enc1, dec3), dim=1)

        dec4 = self.decoder4(dec3)

        output = self.final_conv(dec4)
        output = self.sigmoid(output)

        return output

model = UNet()
model.load_state_dict(torch.load('dotted_image_cnn_7.pth', map_location=device))
model = model.to(device)
model.eval()

def predict(image):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize if needed
        transforms.ToTensor()
    ])
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image).squeeze(0).cpu()
        output_image = transforms.ToPILImage()(output)
        return output_image

def resize_image(image):
    if image is None:
        raise ValueError("The image is empty. Please check the image path.")
    
    # modify the dimensions
    original_height, original_width = image.shape[:2]
    new_height = math.ceil(original_height / 256) * 256
    new_width = math.ceil(original_width / 256) * 256

    # Resize the image
    resized_img = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return resized_img

# Function to split the frame into smaller images
def split_image(image):
    height, width, _ = image.shape
    sub_images = []
    step = 256  # Step size should be 256 to avoid overlapping

    for i in range(0, height - 256 + 1, step):
        for j in range(0, width - 256 + 1, step):
            sub_img = image[i:i + 256, j:j + 256]
            if sub_img.shape == (256, 256, 3):
                sub_images.append([sub_img, i // 256, j // 256])

    return sub_images

# Function to count people in a small image using cv2 script
def count_red_dots(image):
    count = 0
    image = np.array(image)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Define the target color in HSV format
    lower_red = np.array([0, 160, 155])
    upper_red = np.array([179, 230, 255])

    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Find contours of potential red dots
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = len(contours)
    return count

def process_image(image):
    if image is None:
        raise ValueError("The image is empty. Please check the image path.")

    modified_images = []

    # Step 1: Resize the image
    resized_image = resize_image(image)

    # Step 2: Split the resized image into sub-images
    sub_images = split_image(resized_image)

    # Step 3: Pass the sub-images to the GAN model to add labels
    for sub_image, row, col in sub_images:
        modified_img = predict(sub_image)
        modified_images.append([modified_img, row, col])

    # Step 4: Pass the modified images to the contour detection function
    height = max(info[1] for info in modified_images) + 1
    width = max(info[2] for info in modified_images) + 1
    matrix = np.zeros((height, width), dtype=int)

    for modified_img, row, col in modified_images:
        red_dot_count = count_red_dots(modified_img)
        matrix[row, col] = red_dot_count

    count = np.sum(matrix)
    return count



def process_videos(video):
    try:
        thumbnails = video.thumbnails.all()

        for thumbnail in thumbnails:
            # Assuming each Thumbnail has one image associated with it
            image_path = os.path.join(BASE_DIR, thumbnail.image.url.lstrip('/'))
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Image at path {image_path} could not be loaded. Please check the path.")
            
            # Process the image using your model
            count = process_image(img)
            
            # Update the Thumbnail object with the processed result
            thumbnail.result = count
            thumbnail.save()

    except Exception as e:
        print(f"Error processing videos: {str(e)}")


