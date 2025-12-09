import argparse
from . import TelemetryAgent, generate_scenario

INTFS = ['eth0', 'wifi0', 'lte0', 'sat0']

def main():
    parser = argparse.ArgumentParser(
        description='Hoplynk Telemetry Agent - Edge Link Health Scoring',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'command',
        choices=['run'],
        help='Run the agent on scenario A | B | C'
    )

    parser.add_argument(
        '--scenario',
        choices=['A', 'B', 'C'],
        required=True,
        help='Scenario to run (A: Gradual Degradation, B: Noisy Spikes, C: Misleading Throughput)'
    )

    args = parser.parse_args()

    if args.command == 'run':
        run_scenario(args.scenario)

def run_scenario(scenario: str):
    """Run a simulation of the specified scenario"""
    print(f"=== Hoplynk Telemetry Agent - Scenario {scenario} ===\n")

    agent = TelemetryAgent(INTFS)
    samples = generate_scenario(scenario)

    score_history = {name: [] for name in INTFS}

    # --- Simulation Loop ---
    for t in range(90):
        for intf_name in INTFS:
            sample = samples[intf_name][t]
            agent.process_sample(intf_name, sample)
            score_history[intf_name].append(agent.interfaces[intf_name].curr_score)

        # Print status every 10 seconds
        if (t + 1) % 10 == 0:
            print(f"\n--- Time: {t + 1}s ---")
            for name in INTFS:
                intf = agent.interfaces[name]
                status_icon = {
                    'HEALTHY': '✓',
                    'DEGRADED': '!',
                    'DOWN': '✗'
                }[intf.curr_status.name]
                print(f"{name:8s} {status_icon} [{intf.curr_status.name:9s}] Score: {intf.curr_score:.3f}")

    # End-of-run summary
    print(f"\n{'='*30}")
    print("SCENARIO SUMMARY")
    print(f"{'='*30}")

    # Calculate and rank interfaces by average score
    avg_scores = {name: sum(scores) / len(scores) for name, scores in score_history.items()}
    ranked = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)

    print("\nInterface Rankings (by average score):")
    for rank, (name, avg_score) in enumerate(ranked, 1):
        print(f"  {rank}. {name:8s}  {avg_score:.3f}")
