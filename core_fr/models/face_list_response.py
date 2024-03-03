import string
from datetime import datetime
from typing import List


class FaceListResponse:
    def __init__(self):
        self.success = False
        self.faces: List[string] = []
        self.processMs = 0
        self.moduleId = ""
        self.moduleName = ""
        self.code = 0
        self.command = ""
        self.err_trace = ""
        self.error = ""
        self.requestId = ""
        self.inferenceDevice = ""
        self.analysisRoundTripMs = 0
        self.processedBy = ""
        self.timestampUTC = datetime.now()
