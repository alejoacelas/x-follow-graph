import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.follow = json.loads((ROOT / "data/raw/following.json").read_text())
        cls.posts = json.loads((ROOT / "data/raw/post-features.json").read_text())
        cls.candidates = json.loads((ROOT / "data/raw/candidates.json").read_text())

    def test_following_is_unique_and_complete_snapshot(self):
        handles = [x["handle"].lower() for x in self.follow["accounts"]]
        self.assertEqual(len(handles), 443)
        self.assertEqual(len(handles), len(set(handles)))

    def test_posts_are_bounded_and_have_no_full_text(self):
        for account in self.posts["accounts"]:
            self.assertLessEqual(account["post_count"], 20)
            self.assertEqual(account["post_count"], len(account["posts"]))
            for post in account["posts"]:
                self.assertNotIn("text", post)

    def test_candidates_are_not_already_followed(self):
        followed = {x["handle"].lower() for x in self.follow["accounts"]}
        self.assertTrue(all(x["handle"].lower() not in followed for x in self.candidates["accounts"]))


if __name__ == "__main__":
    unittest.main()
