import unittest

from telemetry_agent import Status, TelemetryAgent


class TestHysteresis(unittest.TestCase):

    def test_requires_consecutive_samples(self):
        # Test that status changes require 5 consecutive samples
        agent = TelemetryAgent(['test0'])
        intf = agent.interfaces['test0']
    
        self.assertEqual(intf.curr_status, Status.HEALTHY)
    
        # Send 4 `DEGRADED` scores (not enough to transition)
        for i in range(4):
            agent.update_status(intf, 0.3, float(i))
        self.assertEqual(intf.curr_status, Status.HEALTHY)

        # 5th `DEGRADED` score triggers transition
        agent.update_status(intf, 0.3, 4.0)
        self.assertEqual(intf.curr_status, Status.DEGRADED)
    
    def test_resets_counter_on_status_match(self):
        # Counter should reset if score returns to current status range
        agent = TelemetryAgent(['test0'])
        intf = agent.interfaces['test0']

        self.assertEqual(intf.curr_status, Status.HEALTHY)

        # Send 3 `DEGRADED` scores
        for i in range(3):
            agent.update_status(intf, 0.3, float(i))
        self.assertEqual(intf.degraded_ct, 3)

        # Send 1 `HEALTHY` score (resets counter)
        agent.update_status(intf, 0.8, 3.0)
        self.assertEqual(intf.degraded_ct, 0)
        self.assertEqual(intf.healthy_ct, 1)

        self.assertEqual(intf.curr_status, Status.HEALTHY)


class TestStatusTransitions(unittest.TestCase):

    def test_healthy_to_down(self):
        agent = TelemetryAgent(['test0'])
        intf = agent.interfaces['test0']

        # Start HEALTHY
        self.assertEqual(intf.curr_status, Status.HEALTHY)

        # Send 5 consecutive bad scores
        for i in range(3):
            agent.update_status(intf, 0.4, float(i))
        for i in range(3, 5):
            agent.update_status(intf, 0.0, float(i))

        self.assertEqual(intf.curr_status, Status.DEGRADED)
        self.assertEqual(intf.degraded_ct, 5)
        self.assertEqual(intf.down_ct, 2)

        # Send 8 `DOWN` scores
        for i in range(5, 13):
            agent.update_status(intf, 0.0, float(i))

        self.assertEqual(intf.curr_status, Status.DOWN)
        self.assertEqual(intf.degraded_ct, 13)
        self.assertEqual(intf.down_ct, 10)
    
    def test_down_to_healthy(self):
        agent = TelemetryAgent(['test0'])
        intf = agent.interfaces['test0']

        # Start DOWN
        intf.curr_status = Status.DOWN

        # Send 1 `HEALTHY` score
        agent.update_status(intf, 0.8, 0.0)

        self.assertEqual(intf.curr_status, Status.DEGRADED)
        self.assertEqual(intf.degraded_ct, 0)
        self.assertEqual(intf.healthy_ct, 1)

        # Send 2 `DOWN` scores
        for i in range(1, 3):
            agent.update_status(intf, 0.0, float(i))

        self.assertEqual(intf.curr_status, Status.DEGRADED)
        self.assertEqual(intf.down_ct, 2)
        self.assertEqual(intf.degraded_ct, 2)
        self.assertEqual(intf.healthy_ct, 0)

        # Send 1 `DEGRADED` score
        agent.update_status(intf, 0.3, 3.0)

        self.assertEqual(intf.curr_status, Status.DEGRADED)
        self.assertEqual(intf.down_ct, 0)
        self.assertEqual(intf.degraded_ct, 3)

        # Send 5 `HEALTHY` scores
        for i in range(4, 9):
            agent.update_status(intf, 1.0, float(i))

        self.assertEqual(intf.curr_status, Status.HEALTHY)
        self.assertEqual(intf.healthy_ct, 5)
