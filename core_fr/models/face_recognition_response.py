from typing import List
from datetime import datetime


class PredictionResponse:
    def __init__(self):
        self.confidence = 0.0
        self.userid = ""
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0


class FaceRecognitionResponse:
    def __init__(self):
        self.message = ""
        self.count = 0
        self.predictions: List[PredictionResponse] = []
        self.success = False
        self.inferenceMs = 0
        self.processMs = 0
        self.moduleId = ""
        self.moduleName = ""
        self.code = 0
        self.command = ""
        self.requestId = ""
        self.inferenceDevice = ""
        self.analysisRoundTripMs = 0
        self.processedBy = ""
        self.timestampUTC = datetime.now()
