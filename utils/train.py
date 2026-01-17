from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader
from ultralytics import YOLO

from annotations import Annotation

def prepare_datasets(annotations: list[Annotation], test_size=0.2, val_size=0.1):
    """Podział danych na zestawy treningowe, walidacyjne i testowe"""
    train, temp = train_test_split(annotations, test_size=test_size + val_size, random_state=42)
    val, test = train_test_split(temp, test_size=val_size/(test_size + val_size), random_state=42)
    return train, val, test

model = YOLO("../yolo11n.pt")

# Train the model
results = model.train(data="data.yaml", epochs=100, imgsz=640)

# Evaluate the model's performance on the validation set
metrics = model.val()
print(metrics)

# Perform object detection on an image
prediction = model("photos/1.jpg")  # Predict on an image
prediction[0].show()  # Display results

# Export the model to ONNX format for deployment
path = model.export(format="onnx")  # Returns the path to the exported model