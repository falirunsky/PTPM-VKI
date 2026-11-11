import unittest
from pathlib import Path

from src.database import DatabaseRepository
from src.parser import ForumParser


FIXTURES = Path(__file__).parent / "fixtures"


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        self.html = (FIXTURES / "sample_page.html").read_text(encoding="utf-8")

    def test_parse_html_extracts_only_valid_comments(self):
        data = self.parser.parse_html(self.html)
        self.assertEqual(len(data), 3)
        self.assertEqual([d["id"] for d in data], [1, 2, 3])

    def test_parse_html_preserves_html_markup(self):
        data = self.parser.parse_html(self.html)
        first = data[0]
        self.assertEqual(first["id"], 1)
        self.assertEqual(first["name"], "alice")
        self.assertIn("<b>world</b>", first["message"])
        third = data[2]
        self.assertIn("<i>alice</i>", third["message"])

    def test_parse_html_returns_empty_for_no_comments(self):
        self.assertEqual(self.parser.parse_html("<html><body></body></html>"), [])

    def test_save_to_db_persists_all_records(self):
        data = self.parser.parse_html(self.html)
        repo = DatabaseRepository(":memory:")
        try:
            count = self.parser.save_to_db(data, repo)
            self.assertEqual(count, 3)
            self.assertEqual(len(repo.get_by_name("alice")), 2)
            self.assertEqual(repo.get_by_id(2)["name"], "bob")
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()