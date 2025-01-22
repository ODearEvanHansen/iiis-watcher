import pytest
from unittest.mock import patch, Mock
from iiis_watcher.main import get_seminar_items, check_for_updates
import os

@pytest.fixture
def mock_html():
    return '''
    <div class="seminar-item">
        <div class="title">Test Seminar</div>
        <div class="date">2025-01-01</div>
        <div class="speaker">Test Speaker</div>
        <div class="abstract">Test abstract</div>
    </div>
    '''

def test_get_seminar_items(mock_html):
    with patch('requests.get') as mock_get, \
         patch('bs4.BeautifulSoup') as mock_soup:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        seminars = get_seminar_items()
        assert len(seminars) == 1
        assert seminars[0]['title'] == 'Test Seminar'
        assert seminars[0]['date'] == '2025-01-01'
        assert seminars[0]['speaker'] == 'Test Speaker'
        assert seminars[0]['abstract'] == 'Test abstract'

def test_check_for_updates_new_seminar():
    with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
         patch('iiis_watcher.main.send_email') as mock_send, \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock seminar data
        mock_get.return_value = [{
            'title': 'New Seminar',
            'date': '2025-01-01',
            'speaker': 'New Speaker',
            'abstract': 'New abstract'
        }]
        
        # Mock file operations
        mock_open.return_value.read.return_value = ''
        
        check_for_updates()
        
        # Verify email was sent
        mock_send.assert_called_once()
        assert 'New Seminar' in mock_send.call_args[0][1]

def test_check_for_updates_no_new_seminars():
    with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
         patch('iiis_watcher.main.send_email') as mock_send, \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock seminar data
        mock_get.return_value = [{
            'title': 'Existing Seminar',
            'date': '2025-01-01',
            'speaker': 'Existing Speaker',
            'abstract': 'Existing abstract'
        }]
        
        # Mock file operations
        mock_open.return_value.read.return_value = '2025-01-01-Existing Seminar\n'
        
        check_for_updates()
        
        # Verify no email was sent
        mock_send.assert_not_called()

def test_check_for_updates_file_creation(tmpdir):
    with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
         patch('iiis_watcher.main.send_email'):
        
        # Set up temp directory
        os.chdir(tmpdir)
        
        # Mock seminar data
        mock_get.return_value = [{
            'title': 'New Seminar',
            'date': '2025-01-01',
            'speaker': 'New Speaker',
            'abstract': 'New abstract'
        }]
        
        check_for_updates()
        
        # Verify file was created
        assert os.path.exists('seen_seminars.txt')
        with open('seen_seminars.txt') as f:
            assert '2025-01-01-New Seminar' in f.read()