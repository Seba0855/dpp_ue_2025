from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader
from ultralytics import YOLO

from annotations import Annotation, parse_annotations


def prepare_datasets(annotations: list[Annotation], test_size=0.2, val_size=0.1):
    """Podział danych na zestawy treningowe, walidacyjne i testowe"""
    train, temp = train_test_split(annotations, test_size=test_size + val_size, random_state=42)
    val, test = train_test_split(temp, test_size=val_size/(test_size + val_size), random_state=42)
    return train, val, test

# annotations = parse_annotations(annotations_file_path="../photos/annotations.xml", images_dir="photos/")
# train, val, test = prepare_datasets(annotations)

model = YOLO("yolo26n.pt")

# Optymalizacje dla CPU - większy batch size i workers
results = model.train(
    data="data.yaml", 
    epochs=100, 
    imgsz=640, 
    optimizer="MuSGD", 
    device="cpu",
    batch=32,  # Większy batch size
    workers=8,  # Więcej workerów dla ładowania danych
    amp=False   # Wyłącz mixed precision na CPU
)

# Evaluate the model's performance on the validation set
metrics = model.val()
print(metrics)

# Perform object detection on an image
prediction = model("photos/1.jpg")  # Predict on an image
prediction[0].show()  # Display results

# Export the model to ONNX format for deployment
# path = model.export(format="onnx")  # Returns the path to the exported model