import unittest

class card_test(unittest.TestCase):
    def test_create_card(self):
        deck = get_deck()
        self.assertEqual(52, len(deck))

if __name__ == '__main__':
    unittest.main()
