import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.watcher import check_for_updates

def test_check_for_updates():
    # Fetch actual seminar data
    seminars = check_for_updates()
    
    # Basic validation of the results
    assert isinstance(seminars, list), "Expected a list of seminars"
    
    if seminars:  # If there are seminars listed
        for seminar in seminars:
            assert isinstance(seminar, str), "Each seminar should be a string"
            assert len(seminar) > 10, "Seminar description seems too short"
            
        # Check for specific known elements (if any)
        assert any("IIIS" in seminar for seminar in seminars), "Expected to find IIIS-related content"
        
    # If no seminars, that's also a valid state (e.g., during holidays)
    else:
        print("No seminars found - this might be expected during certain periods")