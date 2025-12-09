# === Network metric scenarios ===

SCENARIOS = {
    # Scenario A: Gradual Degradation + Recovery
    'A': {
        'eth0': {
            'baseline': {'rtt': 15, 'throughput': 150, 'loss': 0.5, 'jitter': 5},
        },
        'wifi0': {
            'baseline': {'rtt': 30, 'throughput': 100, 'loss': 1, 'jitter': 10},
            'phases': [
                # (start_t, end_t, target_metrics)
                (15, 50, {'rtt': 240, 'throughput': 40, 'loss': 12, 'jitter': 50}),  # Degrade
                (50, 90, {'rtt': 30, 'throughput': 100, 'loss': 1, 'jitter': 10}),   # Recover
            ]
        },
        'lte0': {
            'baseline': {'rtt': 120, 'throughput': 60, 'loss': 3, 'jitter': 25},
        },
        'sat0': {
            'baseline': {'rtt': 600, 'throughput': 30, 'loss': 2, 'jitter': 40},
        },
    },

    # Scenario B: Noisy Spikes (Flap Trap)
    'B': {
        'eth0': {
            'baseline': {'rtt': 15, 'throughput': 150, 'loss': 0.5, 'jitter': 5},
        },
        'wifi0': {
            'baseline': {'rtt': 30, 'throughput': 100, 'loss': 1, 'jitter': 10},
            'spikes': [
                # (start_t, end_t, spike_metrics)
                (16, 19, {'rtt': 180, 'throughput': 45, 'loss': 12, 'jitter': 55}),  # Moderate spike
                (32, 35, {'rtt': 220, 'throughput': 35, 'loss': 18, 'jitter': 70}),  # Severe spike
                (45, 48, {'rtt': 160, 'throughput': 50, 'loss': 10, 'jitter': 50}),  # Mild spike
                (61, 66, {'rtt': 200, 'throughput': 40, 'loss': 15, 'jitter': 65}),  # Sustained spike
                (75, 78, {'rtt': 190, 'throughput': 42, 'loss': 14, 'jitter': 60}),  # Moderate spike
            ]
        },
        'lte0': {
            'baseline': {'rtt': 120, 'throughput': 60, 'loss': 3, 'jitter': 25},
        },
        'sat0': {
            'baseline': {'rtt': 600, 'throughput': 30, 'loss': 2, 'jitter': 40},
        },
    },

    # Scenario C: Misleading Throughput
    'C': {
        'eth0': {
            'baseline': {'rtt': 15, 'throughput': 150, 'loss': 0.5, 'jitter': 5},
        },
        'wifi0': {
            'baseline': {'rtt': 35, 'throughput': 70, 'loss': 1, 'jitter': 12},
        },
        'lte0': {
            'baseline': {'rtt': 100, 'throughput': 120, 'loss': 10, 'jitter': 70},
        },
        'sat0': {
            'baseline': {'rtt': 620, 'throughput': 50, 'loss': 1.5, 'jitter': 35},
        },
    }
}
