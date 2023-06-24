import unittest
from livescore_api import json_formatter, livescore, Make


class LivescoreTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_retrieve_matches_online(self):
        r"""Fetches matches online"""
        matches = livescore()(max=2)
        self.assertIsInstance(matches, list)
        self.assertIs(type(matches[0]), dict)

    def test_make_predictions(self):
        r"""Makes prediction"""
        matches = [{"Home": "Arsenal", "Away": "Liverpool"}]
        bet = Make(matches, net=False)(progress_bar=False)
        self.assertIsInstance(bet, list)
        self.assertIsInstance(bet[0], dict)
        self.assertIsNotNone(bet[0].get("pick"))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
