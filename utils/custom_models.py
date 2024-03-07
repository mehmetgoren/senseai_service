class SenseAiConfig:
    def __init__(self):
        self.fr_enabled: bool = False
        self.fr_threshold: float = .4

        self.fd_enabled: bool = False
        self.fd_threshold: float = .4

        self.od_enabled: bool = False
        self.od_threshold: float = .4

        self.alpr_enabled: bool = False
        self.alpr_threshold: float = .4
