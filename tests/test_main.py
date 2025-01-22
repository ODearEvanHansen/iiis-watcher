import unittest
from unittest.mock import patch, MagicMock
from iiis_watcher.main import get_seminar_items, check_for_updates, load_previous_items, save_previous_items

class TestMain(unittest.TestCase):
    def test_get_seminar_items(self):
        items = get_seminar_items()
        self.assertIsInstance(items, list)
        for item in items:
            self.assertIn('title', item)
            self.assertIn('date', item)
            self.assertIn('speaker', item)

    @patch('iiis_watcher.main.send_email')
    @patch('iiis_watcher.main.get_seminar_items')
    def test_check_for_updates(self, mock_get_seminar_items, mock_send_email):
        mock_get_seminar_items.return_value = [
            {'title': 'New Seminar', 'date': '2023-10-01', 'speaker': 'New Speaker'}
        ]
        check_for_updates()
        mock_send_email.assert_called_once()

    def test_load_and_save_previous_items(self):
        test_items = [{'title': 'Test', 'date': '2023-10-01', 'speaker': 'Test Speaker'}]
        save_previous_items(test_items)
        loaded_items = load_previous_items()
        self.assertEqual(loaded_items, test_items)

if __name__ == "__main__":
    unittest.main()