import torch
import json
from transformers import FlavaProcessor, FlavaModel
from torch.utils.data import Dataset, DataLoader
import numpy as np
import random
import datetime
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device:", device)

class PlaceholderModel(torch.nn.Module):
    def __init__(self):
        super(PlaceholderModel, self).__init__()
        self.dummy_layer = torch.nn.Linear(768, 570)  # Placeholder layer

    def forward(self, x):
        return self.dummy_layer(x)

class MetallographicDataset(Dataset):
    def __init__(self, data):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        image_path = sample['image']
        grade_and_process = torch.tensor([float(g) for g in sample['grade']] + [float(p) for p in sample['process']])
        inputs = {'image_path': image_path, 'grade_and_process': grade_and_process}
        labels = torch.tensor(sample['friction_list'], dtype=torch.float)
        return {**inputs, "labels": labels}

model_path = "../../models/facebook-flava-full"
processor = FlavaProcessor.from_pretrained(model_path)
flava_model = FlavaModel.from_pretrained(model_path).to(device)

data_path = "../../datasets/data/test/data_friction.json"
with open(data_path, 'r') as f:
    data = json.load(f)

test_dataset = MetallographicDataset(data)
num_test = 100
random_indices = random.sample(range(len(test_dataset)), num_test)
test_subset = torch.utils.data.Subset(test_dataset, random_indices)
test_loader = DataLoader(test_subset, batch_size=1, shuffle=False)

model = PlaceholderModel().to(device)
model.eval()

total_samples = 0
correct_predictions = 0
total_samples_mae = 0
total_mae = 0.0

predictions = []
simil_total = []

def draw_pic(predictions, labels):
    x = np.arange(1, len(predictions) + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(x, predictions, label='Predictions', color='blue')
    plt.plot(x, labels, label='Labels', color='orange')
    plt.legend()
    plt.title('Predictions vs. Labels')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

with torch.no_grad():
    for batch in test_loader:
        image_paths = batch['image_path']
        text_features = batch['grade_and_process'].to(device)

        images = [Image.open(image_path).convert("RGB") for image_path in image_paths]
        flava_inputs = processor(text=[str(text) for text in text_features],
                                 images=images,
                                 return_tensors="pt",
                                 padding=True).to(device)

        outputs = flava_model(**flava_inputs)
        multimodal_embeddings = outputs.multimodal_embeddings.to(device)

        desired_length = 300
        if multimodal_embeddings.size(1) > desired_length:
            multimodal_embeddings = multimodal_embeddings[:, :desired_length, :]
        elif multimodal_embeddings.size(1) < desired_length:
            padding_size = desired_length - multimodal_embeddings.size(1)
            padding = torch.zeros(multimodal_embeddings.size(0), padding_size, multimodal_embeddings.size(2)).to(device)
            multimodal_embeddings = torch.cat((multimodal_embeddings, padding), dim=1)

        predictions = model(multimodal_embeddings)
        labels = batch['labels'].to(device)

        simil = 0.2
        if predictions.size(1) != labels.size(1):
            min_size = min(predictions.size(1), labels.size(1))
            predictions = predictions[:, :min_size]
            labels = labels[:, :min_size]
        
        correct = torch.all(torch.abs(predictions - labels) <= simil, dim=1)
        correct_predictions += correct.sum().item()
        total_samples += len(correct)

        mae = torch.abs(predictions - labels).mean().item()
        total_mae += mae
        total_samples_mae += 1

accuracy = correct_predictions / total_samples * 100
print(f"Accuracy: {accuracy:.2f}%")

average_mae = total_mae / total_samples_mae
print(f"Mean Absolute Error (MAE): {average_mae:.4f}")
