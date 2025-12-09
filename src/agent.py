from sampling import Sample, MetricType
from interface import Status, Interface

# [config] Hysteresis parameters
THRESHOLDS = {
    'HEALTHY': 5,
    'DEGRADED': 5,
    'DOWN': 10,
}

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

        # Compute score and update status if necessary
        intf.curr_score = self.compute_health_score(sample)
        self.update_status(intf, intf.curr_score, sample.timestamp)

    def update_status(self, intf: Interface, new_score: float, timestamp: float):
        """Apply hysteresis to prevent status flapping under noisy measurements"""
        match Status.from_score(new_score):
            case Status.HEALTHY:
                intf.healthy_ct += 1
                intf.degraded_ct = 0
                intf.down_ct = 0
            case Status.DEGRADED:
                intf.healthy_ct = 0
                intf.degraded_ct += 1
                intf.down_ct = 0
            case Status.DOWN:
                intf.healthy_ct = 0
                intf.degraded_ct += 1
                intf.down_ct += 1

        if intf.curr_status == Status.DOWN and not intf.down_ct:
            intf.curr_status = Status.DEGRADED
            self.log_transition(intf.name, Status.DOWN, Status.DEGRADED, timestamp)
            return

        old_status = intf.curr_status

        if intf.down_ct >= THRESHOLDS['DOWN']:
            intf.curr_status = Status.DOWN
        elif intf.degraded_ct >= THRESHOLDS['DEGRADED']:
            intf.curr_status = Status.DEGRADED
        elif intf.healthy_ct >= THRESHOLDS['HEALTHY']:
            intf.curr_status = Status.HEALTHY

        if old_status != intf.curr_status:
            self.log_transition(intf.name, old_status, intf.curr_status, timestamp)

    def log_transition(self, intf_name: str, old_status: Status, new_status: Status, timestamp: float):
        """Print status transition with timestamp and reason"""
        intf = self.interfaces[intf_name]
        print(f"[TRANSITION @ t={timestamp:.1f}s] {intf_name}: {old_status.name} → {new_status.name} "
              f"(H={intf.healthy_ct}, D={intf.degraded_ct}, DN={intf.down_ct})")
