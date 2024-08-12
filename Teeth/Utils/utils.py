from collections import defaultdict

import numpy as np

from Commons.Utils.drawer_utils import get_center


def nms(results):
    best_results = defaultdict(lambda: (None, -1))

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        for i, confidence in enumerate(confidences):
            class_id = int(labels[i])
            if confidence > best_results[class_id][1]:
                best_results[class_id] = (result, confidence, boxes[i])
    return best_results


def nms_tooth_process(results, threshold=0):
    best_results = defaultdict(lambda: (None, -1, None))
    i = 0
    if len(results[0]) != 0:
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            labels = result.boxes.cls.cpu().numpy()
            best_results[i] = (result, confidences[i], boxes[i])

    return best_results


def detect_collisions(data, numbering_keeps):
    collisions = []
    process_name, process_box = data
    process_x1, process_y1, process_x2, process_y2 = process_box
    for tooth_class_id, (_, _, tooth_box) in numbering_keeps.items():
        tooth_x1, tooth_y1, tooth_x2, tooth_y2 = tooth_box
        if (process_x1 < tooth_x2 and process_x2 > tooth_x1 and
                process_y1 < tooth_y2 and process_y2 > tooth_y1):
            collisions.append({
                'tooth_id': tooth_class_id,
                'process_name': process_name,
                'box_data': process_box
            })
    return collisions


def pair_teeth_processes(numbering_keeps, process_keeps, index):
    paired = {}
    single_match_processes = ['dentin-curugu', 'dolgu', 'implant', 'kanal-tedavisi', 'kaplama', 'kirik',
                              'kok-enfeksiyonu']

    multiple_match_processes = ['kopru']

    tooth_results = {index: {
        "image": "",
        "data": [
            {"teeth_number": 11, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 12, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 13, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 14, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 15, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 16, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 17, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 18, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 21, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 22, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 23, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 24, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 25, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 26, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 27, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 28, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 31, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 32, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 33, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 34, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 35, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 36, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 37, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 38, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 41, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 42, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 43, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 44, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 45, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 46, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 47, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
            {"teeth_number": 48, 'status': 'Kayıp Diş', "annotations": [], "illness": []},
        ]}}
    # result['result'][0]['teeth_number']
    for process_class_id, (process_result, _, process_box) in process_keeps.items():
        process_center = get_center(process_box)
        process_name = process_result.names[process_class_id]
        tooth_results[index]["data"][process_class_id]["status"] = "Sağlam diş"
        if process_name in multiple_match_processes:
            collisions = detect_collisions((process_name, process_box), numbering_keeps)
            for result in collisions:
                x1, y1, x2, y2 = result["box_data"]
                tooth_results[index]["data"][int(result['tooth_id'])].append({
                    'process_name': result["process_name"],
                    "x_start": x1,
                    "y_start": y1,
                    "x_end": x2,
                    "y_end": y2
                })

        elif process_name in single_match_processes:
            closest_tooth = min(numbering_keeps.items(),
                                key=lambda t: np.linalg.norm(np.array(process_center) - np.array(get_center(t[1][2]))))
            x1, y1, x2, y2 = process_box
            tooth_results[index]["data"][closest_tooth[0]]["annotations"].append({
                'process_name': process_name,
                "x_start": x1,
                "y_start": y1,
                "x_end": x2,
                "y_end": y2
            })



    return tooth_results
