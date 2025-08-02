"""
Tests for ArchetypeCluster analysis and resonance vector logic.
"""

import unittest
from mvp.archetype_cluster import ArchetypeCluster

class TestArchetypeCluster(unittest.TestCase):
    def setUp(self):
        self.cluster = ArchetypeCluster()
        self.default_profile = self.cluster.default_user_profile()

    def test_analyze_input(self):
        # Analyze input and check Phoenix synthesis
        input_text = "I want to explore new ideas and help others."
        result = self.cluster.analyze_input(input_text, self.default_profile)
        self.assertIn("archetype", result)
        self.assertEqual(result["archetype"], "Phoenix")
        self.assertIn("synthesized_resonance", result)
        self.assertIn("summary", result)
        self.assertIsInstance(result["archetype_outputs"], list)
        self.assertEqual(len(result["archetype_outputs"]), 13)

    def test_update_resonance(self):
        # Update resonance and check vector
        updates = {"Explorer": 0.9, "Nurturer": 0.8}
        updated = self.cluster.update_resonance(self.default_profile.copy(), updates)
        self.assertEqual(updated["Explorer"], 0.9)
        self.assertEqual(updated["Nurturer"], 0.8)

if __name__ == "__main__":
    unittest.main()
