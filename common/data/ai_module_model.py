class AiModuleModel:
    def __init__(self):
        self.name: str = ''
        self.description: str = ''
        self.enabled: bool = False
        self.api_url: str = ''
        self.threshold: float = .4
        self.label_field: str = ''
        self.motion_detection_enabled: bool = False
        self.persistence_enabled: bool = False  # or save on db
        self.notification_enabled: bool = False
