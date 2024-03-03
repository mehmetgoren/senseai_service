from typing import List


class PredictionResponse:
    def __init__(self):
        self.confidence: float = 0
        self.label: str = ''
        self.x_min: int = 0
        self.y_min: int = 0
        self.x_max: int = 0
        self.y_max: int = 0


class ObjectDetectionResponse:
    def __init__(self):
        self.message: str = ''
        self.count: int = 0
        self.predictions: List[PredictionResponse] = []
        self.success: bool = False
        self.processMs: int = 0
        self.inferenceMs: int = 0
        self.moduleId: str = ''
        self.moduleName: str = ''
        self.code: int = 0
        self.command: str = ''
        self.requestId: str = ''
        self.inferenceDevice: str = ''
        self.analysisRoundTripMs: int = 0
        self.processedBy: str = ''
        self.timestampUTC: str = ''
