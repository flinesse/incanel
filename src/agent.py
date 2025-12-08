from sampling import Sample, MetricType
from interface import Status, Interface

class TelemetryAgent:
    def __init__(self, interfaces: list[str], custom_weights: dict[MetricType, float] | None = None):
        self.interfaces = {intf: Interface(intf) for intf in interfaces}

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
        """Process a single sample for the interface corresponding to `intf_name`"""
        intf = self.interfaces[intf_name]
        intf.rolling_window.add_sample(sample)

        # Compute score
        intf.curr_score = self.compute_health_score(sample)

        # TODO: Hysteresis dampening
        if intf.curr_score >= 0.70:
            intf.curr_status = Status.HEALTHY
        elif intf.curr_score >= 0.40:
            intf.curr_status = Status.DEGRADED
        else:
            intf.curr_status = Status.DOWN
