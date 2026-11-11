import unittest

from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    # ---- add ----
    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "alice", "hi"))
        row = self.repo.get_by_id(1)
        self.assertEqual(row, {"id": 1, "name": "alice", "message": "hi"})

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, "alice", "hi")
        with self.assertRaises(ValueError):
            self.repo.add(1, "bob", "hello")

    def test_add_message_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.repo.add(1, "alice", "x" * (DatabaseRepository.MAX_MESSAGE_LEN + 1))

    def test_add_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.repo.add(1, "a" * (DatabaseRepository.MAX_NAME_LEN + 1), "msg")

    def test_add_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.repo.add("1", "alice", "hi")

    # ---- get_by_id ----
    def test_get_by_id_existing(self):
        self.repo.add(5, "carol", "hello")
        self.assertEqual(
            self.repo.get_by_id(5),
            {"id": 5, "name": "carol", "message": "hello"},
        )

    def test_get_by_id_missing_returns_none(self):
        self.assertIsNone(self.repo.get_by_id(999))

    # ---- get_by_name ----
    def test_get_by_name_returns_all_matches(self):
        self.repo.add(1, "alice", "one")
        self.repo.add(2, "bob", "two")
        self.repo.add(3, "alice", "three")
        rows = self.repo.get_by_name("alice")
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["id"] for r in rows}, {1, 3})

    def test_get_by_name_empty_returns_empty_list(self):
        self.assertEqual(self.repo.get_by_name("nobody"), [])

    # ---- update ----
    def test_update_existing(self):
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_missing_returns_false(self):
        self.assertFalse(self.repo.update(42, "value"))

    def test_update_message_too_long_raises(self):
        self.repo.add(1, "alice", "old")
        with self.assertRaises(ValueError):
            self.repo.update(1, "x" * (DatabaseRepository.MAX_MESSAGE_LEN + 1))

    # ---- delete ----
    def test_delete_existing(self):
        self.repo.add(1, "alice", "hi")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.repo.delete(123))


if __name__ == "__main__":
    unittest.main()
