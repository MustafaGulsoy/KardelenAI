import base64
import os

import cv2
from ultralytics import YOLO

from Commons.Utils.converter_utils import convert_to_png_from_url
from .utils import nms, nms_tooth_process, pair_teeth_processes

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Commons', 'Models', 'Teeth')

numbering_model = YOLO(MODEL_PATH + "/ToothNumbering.pt")
process_model = YOLO(MODEL_PATH + "/ProcessDetection.pt")


async def process_xray(image_url, header):
    processed_images = []
    paired_results = []

    images = convert_to_png_from_url(image_url.strip(), header)
    i = 0
    for image in images:

        numbering_results = numbering_model(image)
        process_detection_result = process_model(image)

        numbering_keep = nms(numbering_results)
        process_keep = nms_tooth_process(process_detection_result)
        labels = numbering_results[0].names
        for class_id, (_, confidence, box) in numbering_keep.items():
            x1, y1, x2, y2 = box.astype(int)
            text = f"{labels[class_id]}"
            color = (36, 255, 12) if int(class_id) < 30 else (36, 255, 12)
            cv2.putText(image, text, (int((x1 + x2) / 2) - 4, int((y1 + y2) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        _, buffer = cv2.imencode('.jpg', image)
        processed_image = base64.b64encode(buffer).decode('utf-8')

        paired_result = pair_teeth_processes(numbering_keep, process_keep, i)
        paired_result["image"] = processed_image
        paired_results.append(paired_result)
        processed_images.append(processed_image)
        i = i + 1

    return paired_results


class ToothXRayUtil:
    pass
