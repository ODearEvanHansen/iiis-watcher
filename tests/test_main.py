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
    # Create a mock for the requests.get function
    with patch('requests.get') as mock_get:
        # Create a mock response
        mock_response = Mock()
        mock_response.text = """
        <html>
        <body>
            <div class="seminar-item">
                <div class="title">Test Seminar</div>
                <div class="date">2025-01-01</div>
                <div class="speaker">Test Speaker</div>
                <div class="abstract">Test abstract</div>
            </div>
        </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Call the function with the real implementation
        seminars = get_seminar_items()
        
        # Verify the results
        assert len(seminars) == 1
        assert seminars[0]['title'] == 'Test Seminar'
        assert seminars[0]['date'] == '2025-01-01'
        assert seminars[0]['speaker'] == 'Test Speaker'
        assert seminars[0]['abstract'] == 'Test abstract'

def test_check_for_updates_new_seminar():
    with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
         patch('iiis_watcher.main.send_email') as mock_send, \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock seminar data
        mock_get.return_value = [{
            'title': 'New Seminar',
            'date': '2025-01-01',
            'speaker': 'New Speaker',
            'abstract': 'New abstract'
        }]
        
        # Set up mock file operations
        mock_file = Mock()
        mock_file.read.return_value = ''
        mock_open.return_value.__enter__.return_value = mock_file
        
        check_for_updates()
        
        # Verify email was sent
        mock_send.assert_called_once()
        assert 'New Seminar' in mock_send.call_args[0][1]

def test_check_for_updates_no_new_seminars():
    with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
         patch('iiis_watcher.main.send_email') as mock_send, \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock seminar data
        mock_get.return_value = [{
            'title': 'Existing Seminar',
            'date': '2025-01-01',
            'speaker': 'Existing Speaker',
            'abstract': 'Existing abstract'
        }]
        
        # Set up mock file operations
        mock_file = Mock()
        mock_file.read.return_value = '2025-01-01-Existing Seminar\n'
        mock_open.return_value.__enter__.return_value = mock_file
        
        check_for_updates()
        
        # Verify no email was sent
        mock_send.assert_not_called()

def test_check_for_updates_file_creation(tmpdir):
    # Set up temp directory
    original_dir = os.getcwd()
    os.chdir(tmpdir)
    
    try:
        # Make sure the file doesn't exist
        if os.path.exists('seen_seminars.txt'):
            os.remove('seen_seminars.txt')
        
        # Mock the get_seminar_items function
        with patch('iiis_watcher.main.get_seminar_items') as mock_get, \
             patch('iiis_watcher.main.send_email') as mock_send:
            
            # Mock seminar data
            mock_get.return_value = [{
                'title': 'New Seminar',
                'date': '2025-01-01',
                'speaker': 'New Speaker',
                'abstract': 'New abstract'
            }]
            
            # Run the function
            check_for_updates()
            
            # Verify file was created
            assert os.path.exists('seen_seminars.txt')
            with open('seen_seminars.txt') as f:
                content = f.read()
                assert '2025-01-01-New Seminar' in content
            
            # Verify email was sent
            mock_send.assert_called_once()
    finally:
        # Restore original directory
        os.chdir(original_dir)