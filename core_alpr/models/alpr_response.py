from datetime import datetime
from typing import List


class AlprPredictionResponse:
    def __init__(self):
        self.confidence = 0.0
        self.label = ""
        self.plate = ""
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0


class AlprResponse:
    def __init__(self):
        self.success = False
        self.processMs = 0
        self.inferenceMs = 0
        self.predictions: List[AlprPredictionResponse] = []
        self.message = ""
        self.moduleId = ""
        self.moduleName = ""
        self.code = 0
        self.command = ""
        self.requestId = ""
        self.inferenceDevice = ""
        self.analysisRoundTripMs = 0
        self.processedBy = ""
        self.timestampUTC = datetime.now()
