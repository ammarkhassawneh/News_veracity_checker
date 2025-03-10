from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient for the FastAPI application
client = TestClient(app)

def test_verify_news():
    """
    This test checks the /news/verify endpoint using a sample news payload.
    It verifies that the response status is 200 and that the response JSON includes:
    - 'id': the unique identifier for the news entry.
    - 'veracity_score': the confidence score from the analysis.
    - 'is_fake': a boolean indicating whether the news is fake.
    - 'analysis_report': a detailed report of the analysis.
    """
    payload = {
        "title": "Test News Article",
        "content": "This is a sample test news content. " * 15,  # Multiply to ensure enough content length
        "source": "Test Source"
    }
    response = client.post("/news/verify", json=payload)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert "id" in data, "Response should contain 'id'"
    assert "veracity_score" in data, "Response should contain 'veracity_score'"
    assert "is_fake" in data, "Response should contain 'is_fake'"
    assert "analysis_report" in data, "Response should contain 'analysis_report'"
