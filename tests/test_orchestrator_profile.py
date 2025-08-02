"""
Tests for VERN Orchestrator, user profile persistence, and emotion/trait adaptation.
"""

import unittest
from mvp.orchestrator import orchestrator_respond
from mvp.user_profile import load_user_profile, save_user_profile
from mvp.archetype_cluster import ArchetypeCluster

class TestOrchestratorProfile(unittest.TestCase):
    def setUp(self):
        self.user_id = "test_user"
        self.cluster = ArchetypeCluster()
        self.default_profile = self.cluster.default_user_profile()
        save_user_profile(self.user_id, self.default_profile)

    def test_orchestrator_response_and_profile_persistence(self):
        # Initial profile
        profile = load_user_profile(self.user_id, self.default_profile)
        self.assertEqual(profile["Nurturer"], 0.5)
        # Send input and check orchestrator response
        response = orchestrator_respond("I feel joyful and want to help others.", context={}, agent_status=None, user_id=self.user_id)
        self.assertIn("[Phoenix Synthesis]:", response)
        # Profile should persist unchanged unless explicitly updated
        updated_profile = load_user_profile(self.user_id, self.default_profile)
        self.assertEqual(updated_profile["Nurturer"], 0.5)

    def test_profile_persistence(self):
        # Update and reload
        profile = load_user_profile(self.user_id, self.default_profile)
        profile["Challenger"] = 0.9
        save_user_profile(self.user_id, profile)
        loaded = load_user_profile(self.user_id, self.default_profile)
        self.assertEqual(loaded["Challenger"], 0.9)

if __name__ == "__main__":
    unittest.main()
