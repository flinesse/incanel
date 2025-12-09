import unittest

from telemetry_agent import (
    MetricType,
    Status,
    Sample,
    SampleWindow,
)


class TestMetricType(unittest.TestCase):

    def test_normalization(self):
        # Higher is better
        self.assertAlmostEqual(MetricType.THROUGHPUT.normalize(0), 0.0)
        self.assertAlmostEqual(MetricType.THROUGHPUT.normalize(200), 1.0)
        self.assertAlmostEqual(MetricType.THROUGHPUT.normalize(40), 0.2)
        self.assertAlmostEqual(MetricType.THROUGHPUT.normalize(160), 0.8)

        # Lower is better
        self.assertAlmostEqual(MetricType.RTT.normalize(10), 1.0)
        self.assertAlmostEqual(MetricType.PACKET_LOSS.normalize(30), 0.0)
        self.assertAlmostEqual(MetricType.JITTER.normalize(100), 0.5)


class TestStatus(unittest.TestCase):

    def test_from_score_healthy(self):
        self.assertEqual(Status.from_score(0.80), Status.HEALTHY)
        self.assertEqual(Status.from_score(0.61), Status.HEALTHY)
    
    def test_from_score_degraded(self):
        self.assertEqual(Status.from_score(0.60), Status.DEGRADED)
        self.assertEqual(Status.from_score(0.30), Status.DEGRADED)
        self.assertEqual(Status.from_score(0.01), Status.DEGRADED)
    
    def test_from_score_down(self):
        self.assertEqual(Status.from_score(0.0), Status.DOWN)


class TestRollingWindow(unittest.TestCase):

    def test_bounded_memory(self):
        window = SampleWindow()
    
        # Add 100 samples
        for i in range(100):
            sample = Sample.create(i, 50.0, 100.0, 1.0, 10.0)
            window.add_sample(sample)

        # Should only keep 45
        self.assertEqual(len(window.samples), 45)
        self.assertEqual(window.samples[0].timestamp, 55)
        self.assertEqual(window.samples[-1].timestamp, 99)
