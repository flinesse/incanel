from typing import Self
from enum import Enum
from sampling import SampleWindow


class Status(Enum):
    """Interface health status with lower-bound threshold for transitions"""
    HEALTHY = (0.60,)        # 0.60 < score <= 1.0 -> HEALTHY
    DEGRADED = (0.0,)        # 0.0 < score <= 0.60 -> DEGRADED
    DOWN = (float('-inf'),)  # score == 0.0 -> DOWN

    def __init__(self, lb):
        self.lower_bound = lb

    @classmethod
    def from_score(cls, score: float) -> Self:
        """Get status from health score"""
        assert 0.0 <= score <= 1.0

        for status in cls:
            if score > status.lower_bound:
                return status

class Interface:
    def __init__(self, name: str):
        self.name = name
        self.rolling_window = SampleWindow()
        self.curr_score = 0.0
        self.curr_status = Status.HEALTHY
        self.healthy_ct = 0
        self.degraded_ct = 0
        self.down_ct = 0
