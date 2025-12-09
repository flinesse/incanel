from .scenarios import SCENARIOS
from .sampling import Sample


def generate_scenario(scenario: str, duration: int = 90) -> dict[str, list[Sample]]:
    """Generate samples for a given scenario"""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario '{scenario}'. Available: {list(SCENARIOS.keys())}")

    intf_cfg = SCENARIOS[scenario]
    samples = {name: [] for name in intf_cfg}

    for t in range(duration):
        for name, config in intf_cfg.items():
            m = _resolve_metrics(config, t)
            samples[name].append(
                Sample.create(
                    timestamp=t,
                    rtt_ms=m['rtt'],
                    throughput_mbps=m['throughput'],
                    packet_loss_pct=m['loss'],
                    jitter_ms=m['jitter'],
                )
            )

    return samples

def _resolve_metrics(intf_cfg: dict, t: int) -> dict:
    """Resolve metrics for an interface at time t (handles baseline, phases, spikes)

    # Note: Lacks validation and support for mixing; uses linear search
    # for simplicity given small, fixed input sizes
    """
    baseline = intf_cfg['baseline']

    if 'spikes' in intf_cfg:
        for spike_start, spike_end, spike_metrics in intf_cfg['spikes']:
            if spike_start <= t <= spike_end:
                return spike_metrics

        return baseline

    if 'phases' in intf_cfg:
        phases = intf_cfg['phases']

        # Find active phase
        for i, (t_start, t_end, target) in enumerate(phases):
            if t_start <= t < t_end:
                # Interpolate between previous state and target state
                prev = baseline if i == 0 else phases[i - 1][2]
                return {k: _lerp(t, t_start, t_end, prev[k], target[k]) for k in target}

        # After all phases, return last target
        if t >= phases[-1][1]:
            return phases[-1][2]

    return baseline

def _lerp(t: int, t0: int, t1: int, v0: float, v1: float) -> float:
    """Linear interpolation between v0 and v1 as t goes from t0 to t1"""
    if t <= t0:
        return v0
    if t >= t1:
        return v1
    return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
