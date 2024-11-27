import torch
import json
from transformers import FlavaProcessor, FlavaModel
from torch.utils.data import DataLoader

class PlaceholderModel(torch.nn.Module):
    def __init__(self):
        super(PlaceholderModel, self).__init__()
        self.dummy_layer = torch.nn.Linear(768, 14)
    
    def forward(self, x):
        return self.dummy_layer(x)

model_path = "../../models/facebook-flava-full"
processor = FlavaProcessor.from_pretrained(model_path)
flava_model = FlavaModel.from_pretrained(model_path).to(device)

data_path = "../../datasets/data/test/data_cut.json"
with open(data_path, 'r') as f:
    data = json.load(f)

test_dataset = MetallographicDataset(data)
random_indices = random.sample(range(len(test_dataset)), 100)
test_subset = torch.utils.data.Subset(test_dataset, random_indices)
test_loader = DataLoader(test_subset, batch_size=1, shuffle=False)

model = PlaceholderModel().to(device)
model.eval()

total_samples = 0
correct_predictions = 0
total_mae = 0.0

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
        multimodal_embeddings = outputs.last_hidden_state

        predictions = model(multimodal_embeddings)
        labels = batch['labels'].to(device)

        correct = torch.all(torch.abs(predictions - labels) <= 20, dim=1)
        correct_predictions += correct.sum().item()
        total_samples += len(correct)

        mae = torch.abs(predictions - labels).mean().item()
        total_mae += mae

accuracy = correct_predictions / total_samples * 100
average_mae = total_mae / total_samples
print(f"Accuracy: {accuracy:.2f}%")
print(f"Mean Absolute Error (MAE): {average_mae:.4f}")
