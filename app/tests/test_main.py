import pytest
import requests
BASE_URL = "http://localhost:8000"

def test_create_and_redirect():
    """
    Tests the full flow: creating a short link and then using it.
    """
    long_url = "https://www.google.com"
    
    # --- Step 1: Create the short link ---
    response = requests.post(
        f"{BASE_URL}/shorten",
        json={"long_url": long_url}
    )
    
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["long_url"] == long_url
    assert "short_link" in data
    
    short_link = data["short_link"]
    
    short_code = short_link.split("/")[-1]

    # --- Step 2: Use the short link to redirect ---
    # We use allow_redirects=False to inspect the immediate 307 response
    redirect_response = requests.get(
        f"{BASE_URL}/{short_code}",
        allow_redirects=False
    )
    
    # Assert that the status code is a 307 Temporary Redirect
    assert redirect_response.status_code == 307
    
    assert redirect_response.headers["Location"] == long_url


def test_404_not_found():
    """
    Tests that requesting a non-existent short code returns a 404 error.
    """
    non_existent_code = "thisCodeDoesNotExist"
    
    response = requests.get(f"{BASE_URL}/{non_existent_code}")
    
    # Assert that the status code is 404 Not Found
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Short link not found"