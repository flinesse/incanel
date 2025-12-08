from agent import TelemetryAgent
from scenarios import generate_scenario

INTFS = ['eth0', 'wifi0', 'lte0', 'sat0']

def main():
    print("=== Network Telemetry Agent (Sanity Check) ===\n")

    agent = TelemetryAgent(INTFS)
    samples = generate_scenario()

    # --- Simulation START ---
    for t in range(90):
        for intf_name in INTFS:
            sample = samples[intf_name][t]
            agent.process_sample(intf_name, sample)
        
        # Print status every 5 seconds
        if not (t + 1) % 5:
            print(f"\n--- Time: {t + 1}s ---")
            for name in INTFS:
                iface = agent.interfaces[name]
                print(f"{name:8s} [{iface.curr_status.name:9s}] Score: {iface.curr_score:.3f}")

    # --- Simulation END ---

if __name__ == '__main__':
    main()
