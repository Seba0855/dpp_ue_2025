from pathlib import Path
from time import time
import cv2
import numpy as np
from fast_plate_ocr import ONNXPlateRecognizer
from tqdm import tqdm
from ultralytics import YOLO
from fast_alpr import ALPR
import os
from utils.annotations import parse_annotations
from utils.grade import calculate_final_grade
from utils.iou import calculate_iou

class PlateDetector:
    def __init__(self, model: YOLO, annotations_file_path: str, images_dir: str,
                 reader: ONNXPlateRecognizer = ONNXPlateRecognizer('european-plates-mobile-vit-v2-model')):
        self.reader = reader
        self.model = model
        self.annotations = parse_annotations(annotations_file_path, images_dir)
        self._correct = 0
        self._total = 0
        self._ious = []

    def __clean_path_from_extension(self, path: Path) -> str:
        separate_on_dash = path.stem.split('-')[0]
        separate_on_underscore = separate_on_dash.split('_')[0]
        return separate_on_underscore

    def __prediction_cleaner(self, prediction: list[str]) -> str:
        if len(prediction) == 0:
            return "Błąd"
        if prediction[0] == "PL":
            prediction.pop(0)
        if len(prediction) == 0:
            return "Błąd"

        parsed = prediction[0]
        parsed = parsed.replace(' ', '').replace('_', '').replace('|', 'I')
        return parsed

    def __calculate_bounding_box(self, img_path: str, label_path: str):
        with open(label_path) as label_file:
            label_bounding_box_content = label_file.read().strip().split()[1:]
            true_box = list(map(float, label_bounding_box_content))

        w_img, h_img = cv2.imread(str(img_path)).shape[1::-1]
        cx, cy, w, h = true_box
        x1 = (cx - w / 2) * w_img
        y1 = (cy - h / 2) * h_img
        x2 = (cx + w / 2) * w_img
        y2 = (cy + h / 2) * h_img
        return [x1, y1, x2, y2]

    def __carve_plate_from_box(self, prediction_box: list[int], plate_img: np.ndarray):
        x1, y1, x2, y2 = map(int, prediction_box)
        return plate_img[y1:y2, x1:x2]

    def __convert_to_grayscale(self, plate_img: np.ndarray):
        return cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)[..., None]

    def run_single_ocr_prediction(self, img_path: str, label_path: Path):
        prediction_result = self.model.predict(img_path, verbose=False)[0]
        matched_annotation = [ann for ann in self.annotations if
                              (ann.img_path.stem == self.__clean_path_from_extension(label_path))]

        bounding_box = self.__calculate_bounding_box(img_path, label_path.absolute().__str__())

        if len(prediction_result.boxes) > 0:
            prediction_box = prediction_result.boxes.xyxy[0].tolist()
            carved_plate_img = self.__carve_plate_from_box(prediction_box, cv2.imread(img_path))
            ocr_text_output = self.reader.run(self.__convert_to_grayscale(carved_plate_img))

            if not ocr_text_output or not isinstance(ocr_text_output, list):
                text = "Błąd"
            else:
                text = self.__prediction_cleaner(ocr_text_output)

            if text == matched_annotation[0].plate_num:
                self._correct += 1
            else:
                print(f"Predicted: {text}, Correct: {matched_annotation[0].plate_num}")

            self._ious.append(calculate_iou(bounding_box, prediction_box))
        self._total += 1

    def run(self, files: list[Path], labels: list[Path], limit: int = 100):
        print(f"Running OCR on images (limit: {limit})...")
        start = time()
        for index, label_path in enumerate(tqdm(labels[:limit])):
            img_path = Path("photos") / f"{self.__clean_path_from_extension(label_path)}.jpg"
            self.run_single_ocr_prediction(str(img_path), label_path)
        accuracy = (self._correct / self._total) * 100
        mean_iou = sum(self._ious) / len(self._ious) if self._ious else 0
        end = time()

        processing_time = end - start
        print(f"\n OCR Accuracy: {accuracy:.2f}%")
        print(f"Processing time ({self._total} images): {processing_time:.2f} seconds")
        print(f"Mean IoU: {mean_iou:.3f}")
        print(f"Final grade: {calculate_final_grade(accuracy_percent=accuracy, processing_time_sec=processing_time)}")
