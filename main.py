from pathlib import Path
from ultralytics import YOLO
from utils.plate_detector import PlateDetector

model = YOLO("best.pt")
photos = list(Path("photos").glob("*.jpg"))
labels = list(Path("photos/labels").glob("*.txt"))
plate_detector = PlateDetector(model = model, annotations_file_path = "photos/annotations.xml", images_dir = "photos")

# Default limit is 100 images, change this value to process more or fewer images
limit = 100
plate_detector.run(photos, labels, limit)
