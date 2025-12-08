from enum import Enum
from dataclasses import dataclass
from collections import deque

class MetricType(Enum):
    """Metric types with associated normalization bounds and default weights"""
    # min_val, max_val, higher_is_better, default_weight
    RTT = (10.0, 800.0, False, 0.30)        # ms
    THROUGHPUT = (0.0, 200.0, True, 0.25)   # Mb/s
    PACKET_LOSS = (0.0, 30.0, False, 0.30)  # percent
    JITTER = (0.0, 200.0, False, 0.15)      # ms

    def __init__(self, min_val, max_val, higher_is_better, weight):
        self.min_val = min_val
        self.max_val = max_val
        self.higher_is_better = higher_is_better
        self.default_weight = weight

    def normalize(self, value: float) -> float:
        """Normalize value to [0.0, 1.0]"""
        # Clamp and normalize
        clamped = max(self.min_val, min(self.max_val, value))
        normalized = (clamped - self.min_val) / (self.max_val - self.min_val)

        # Invert if lower is better
        if not self.higher_is_better:
            normalized = 1.0 - normalized
        
        return normalized

@dataclass
class Sample:
    timestamp: float
    metrics: dict[MetricType, float]

    @classmethod
    def create(cls, timestamp: float,
               rtt_ms: float,
               throughput_mbps: float,
               packet_loss_pct: float,
               jitter_ms: float):

        return cls(
            timestamp=timestamp,
            metrics={
                MetricType.RTT: rtt_ms,
                MetricType.THROUGHPUT: throughput_mbps,
                MetricType.PACKET_LOSS: packet_loss_pct,
                MetricType.JITTER: jitter_ms,
            }
        )

    def get_metric(self, metric_type: MetricType) -> float:
        return self.metrics[metric_type]

class SampleWindow:

    def __init__(self, capacity: int = 45):
        self.samples = deque(maxlen=capacity)
        # self.win_sum = 0

    def add_sample(self, sample: Sample):
        self.samples.append(sample)

    def is_full(self):
        return len(self.samples) == self.samples.maxlen
