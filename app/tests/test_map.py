import unittest

from app.services.map import generate_map


class TestBoardService(unittest.TestCase):

    def test_generate_map(self):
        """
        Test generate the game map.
        """
        data = generate_map()

        self.assertEqual(len(data), 2)


if __name__ == "__main__":
    unittest.main()
