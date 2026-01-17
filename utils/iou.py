def calculate_iou(bboxA, bboxB):
    xA = max(bboxA[0], bboxB[0])
    yA = max(bboxA[1], bboxB[1])
    xB = min(bboxA[2], bboxB[2])
    yB = min(bboxA[3], bboxB[3])

    inter_area = max(0, xB - xA) * max(0, yB - yA)
    bboxA_area = (bboxA[2] - bboxA[0]) * (bboxA[3] - bboxA[1])
    bboxB_area = (bboxB[2] - bboxB[0]) * (bboxB[3] - bboxB[1])
    union_area = bboxA_area + bboxB_area - inter_area

    return inter_area / union_area if union_area != 0 else 0