"""
Tests for VERN Archetype Cluster, Phoenix synthesis, resonance mapping, and pop culture onboarding.
"""

import unittest
from mvp.archetype_cluster import ArchetypeCluster
from mvp.pop_culture_map import get_archetype_profile_from_character, get_archetype_profile_from_genre

class TestArchetypeCluster(unittest.TestCase):
    def setUp(self):
        self.cluster = ArchetypeCluster()
        self.default_profile = self.cluster.default_user_profile()

    def test_analyze_input(self):
        result = self.cluster.analyze_input("How do I resolve conflict?", self.default_profile)
        self.assertIn("archetype_outputs", result)
        self.assertIn("summary", result)
        self.assertEqual(result["archetype"], "Phoenix")

    def test_update_resonance(self):
        updates = {"Nurturer": 0.8, "Challenger": 0.6}
        updated = self.cluster.update_resonance(self.default_profile.copy(), updates)
        self.assertEqual(updated["Nurturer"], 0.8)
        self.assertEqual(updated["Challenger"], 0.6)

    def test_pop_culture_character(self):
        profile = get_archetype_profile_from_character("Harry Potter")
        self.assertTrue("Sage" in profile and profile["Sage"] > 0.5)

    def test_pop_culture_genre(self):
        profile = get_archetype_profile_from_genre("Fantasy")
        self.assertTrue("Explorer" in profile and profile["Explorer"] > 0.5)

if __name__ == "__main__":
    unittest.main()
