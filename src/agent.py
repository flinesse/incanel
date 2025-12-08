from sampling import Sample, MetricType
from interface import Interface

class TelemetryAgent:
    def __init__(self, custom_weights: dict[MetricType, float] | None = None):
        self.interfaces = {
            'eth0': Interface('eth0'),
            'wifi0': Interface('wifi0'),
            'lte0': Interface('lte0'),
            'sat0': Interface('sat0'),
        }

        if custom_weights:
            self.weights = custom_weights
        else:
            self.weights = {mt: mt.default_weight for mt in MetricType}
    
    def compute_health_score(self, sample: Sample) -> float:
        """Compute metric-weighted health score"""
        score = 0.0

        for metric_type in MetricType:
            raw_val = sample.get_metric(metric_type)
            score += self.weights[metric_type] * metric_type.normalize(raw_val)
        
        return score
    
    def process_sample(self, intf_name: str, sample: Sample):
        # TODO
        pass
