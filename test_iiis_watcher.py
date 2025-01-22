import unittest
from unittest.mock import patch, MagicMock
from iiis_watcher import IIISWatcher

class TestIIISWatcher(unittest.TestCase):
    @patch('iiis_watcher.requests.get')
    def test_fetch_seminars(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response
        
        watcher = IIISWatcher()
        result = watcher.fetch_seminars()
        
        self.assertEqual(result, '<html></html>')
        mock_get.assert_called_once_with(watcher.url)

    @patch('iiis_watcher.smtplib.SMTP')
    def test_send_notification(self, mock_smtp):
        watcher = IIISWatcher()
        test_seminars = ['Seminar 1', 'Seminar 2']
        
        watcher.send_notification(test_seminars)
        
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(
            watcher.email_address, watcher.email_password
        )
        mock_smtp.return_value.send_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()