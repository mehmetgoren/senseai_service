class DetectionBox:
    def __init__(self):
        self.x1: int = 0
        self.y1: int = 0
        self.x2: int = 0
        self.y2: int = 0


class DetectionResult:
    def __init__(self):
        self.pred_cls_name: str = ''
        self.pred_cls_idx: int = 0
        self.pred_score: float = 0.0
        self.box: DetectionBox = DetectionBox()
