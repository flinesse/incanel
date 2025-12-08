import random
from sampling import Sample

def generate_scenario(duration: int = 90):
    samples = {
        'eth0': [],
        'wifi0': [],
        'lte0': [],
        'sat0': [],
    }

    for t in range(duration):
        # eth0: good stable link
        samples['eth0'].append(
            Sample.create(
                timestamp=t,
                rtt_ms=random.uniform(12, 60),
                throughput_mbps=random.uniform(120, 180),
                packet_loss_pct=random.uniform(0.2, 2.0),
                jitter_ms=random.uniform(2, 10),
            )
        )

        # wifi0: moderate with some noise
        samples['wifi0'].append(
            Sample.create(
                timestamp=t,
                rtt_ms=random.uniform(40, 130),
                throughput_mbps=random.uniform(60, 130),
                packet_loss_pct=random.uniform(0.5, 9.0),
                jitter_ms=random.uniform(10, 60),
            )
        )

        # lte0: lower throughput, higher latency
        samples['lte0'].append(
            Sample.create(
                timestamp=t,
                rtt_ms=random.uniform(80, 200),
                throughput_mbps=random.uniform(30, 80),
                packet_loss_pct=random.uniform(2.0, 6.5),
                jitter_ms=random.uniform(20, 60),
            )
        )

        # sat0: consistent high latency
        samples['sat0'].append(
            Sample.create(
                timestamp=t,
                rtt_ms=random.uniform(550, 700),
                throughput_mbps=random.uniform(20, 45),
                packet_loss_pct=random.uniform(6.0, 10.0),
                jitter_ms=random.uniform(30, 50),
            )
        )
    
    return samples
