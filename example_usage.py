from client import AutonomousAIFleetGovernanceCircuitBreaker

def main():
    controller = AutonomousAIFleetGovernanceCircuitBreaker()
    telemetry = {
        "active_agents_count": 8,
        "max_spawn_depth": 3,
        "total_tokens_per_min": 65000,
        "cost_burn_rate_usd_hour": 18.5
    }
    res = controller.evaluate_fleet_governance(telemetry)
    print("--- Century Fleet Governance Monitor ---")
    print(f"Breaker Status: {res['circuit_breaker_state']}")
    print(f"Kill Switch Active: {res['kill_switch_active']}")
    print(f"Metrics: {res['fleet_metrics']}")

if __name__ == "__main__":
    main()
