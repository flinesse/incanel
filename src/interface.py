from enum import Enum
from sampling import SampleWindow

class Status(Enum):
    HEALTHY = 0
    DEGRADED = 1
    DOWN = 2

class Interface:
    def __init__(self, name: str):
        self.name = name
        self.rolling_window = SampleWindow()
        self.curr_score = 0.0
        self.curr_status = Status.HEALTHY
