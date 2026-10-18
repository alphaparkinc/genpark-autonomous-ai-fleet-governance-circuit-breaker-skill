#!/usr/bin/env python3
import json
import sys
from client import AutonomousAIFleetGovernanceCircuitBreaker

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        controller = AutonomousAIFleetGovernanceCircuitBreaker()
        runaway_telemetry = {
            "active_agents_count": 48,
            "max_spawn_depth": 7,
            "total_tokens_per_min": 350000,
            "cost_burn_rate_usd_hour": 140.0
        }
        res = controller.evaluate_fleet_governance(runaway_telemetry)
        assert res["circuit_breaker_state"] == "OPEN_TRIPPED_EMERGENCY_HALT"
        assert res["kill_switch_active"] is True
        assert res["containment_token"] is not None
        print(f"[TEST PASS] Century Controller Tripped: {res['circuit_breaker_state']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-century-fleet-breaker", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_fleet_governance", "description": "Multi-agent fleet governance and emergency kill switch"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                controller = AutonomousAIFleetGovernanceCircuitBreaker()
                out = controller.evaluate_fleet_governance(args.get("fleet_telemetry", {}), args.get("safety_thresholds"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
