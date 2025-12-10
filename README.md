### Running the agent

**Install:**
```bash
# Install in development mode
python -m pip install -e .
````

**Usage:**
```bash
# Run scenario A
telemetry_agent run --scenario A

# Run unit tests
python -m pytest tests/ -v
```

## Design Overview

### Metric Normalization & Scoring

I chose linear normalization for simplicity since we're only looking at four different metrics. In a production scenario, we might consider logarithmic (for RTT) or piecewise based on quality thresholds, which can then be validated against user-reported quality scores.

The rational behind the weights (rtt=0.3, throughput=0.25, loss=0.3, jitter=0.15) was primarily through the lens of real-time applications, which is what Hoplynk is focused on at the moment. For more mission-critical scenarios, the ranking would probably be loss >= rtt > jitter ~= throughput, since we want to prioritize data integrity, reliability, and responsiveness over raw throughput.

### Hysteresis Rules

**State Diagram:**
```
                  5 consecutive ≤ 0.60
            ┌──────────────────────────────┐
            │                              ▼
     ┌──────────┐                    ┌──────────┐
     │ HEALTHY  │                    │ DEGRADED │
     │(0.60,1.0]│                    │(0.0,0.60]│
     └──────────┘                    └──────────┘
         │  ▲                          │  │   ▲
         │  │      5 consecutive       │  │   │
         │  │         > 0.60           │  │   │
         │  └──────────────────────────┘  │   │
         │                                │   │
         │      10 consecutive == 0.0     │   │
         └────────┌───────────────────────┘   │
                  │                           │
                  │                           │
                  ▼                           │
             ┌─────────┐    1 sample > 0.0    │
             │  DOWN   │──────────────────────┘
             │ (= 0.0) │      (immediate)
             └─────────┘

      Note: HEALTHY → DOWN is not a direct transition.
            It will pass through DEGRADED first.
```

- **5 samples @ 1Hz = 5 seconds** — long enough to ignore transient spikes
- **10 samples for DOWN** — higher bar to avoid false positives on link failure
- **Immediate DOWN → DEGRADED** — any sign of life should quickly restore partial service
- **No direct HEALTHY ↔ DOWN** — forces gradual state changes and prevents dramatic flapping; much more realistic


## Production Considerations

For a production Hoplynk device, we would consider:

- A real metric collection infrastructure with configurable sample rates
- Interpolation and insertion sort to address missing and out-of-order samples
- Processing every Nth sample instead or signal upstream producers to slow down while under load/backpressure
- Graceful handling of interface UP/DOWN events. Our system needs to be able to distinguish between "interface is DOWN" (operationally unusable) vs. "interface doesn't exist"
- A watchdog with a heartbeat mechanism to address the agent hanging/crashing itself + a supervisor process to restart on failure
- Metric history for analysis, debugging, and validation
- Observability (structured logging, state snapshots, status APIs for monitoring, etc.)
