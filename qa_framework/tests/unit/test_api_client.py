import pytest
from qa_framework.core.api.client import APIClient
from qa_framework.core.exceptions import APIGatewayError

def test_get_success(mocker):
    """Test a successful GET request."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    
    mocker.patch('requests.Session.request', return_value=mock_response)
    
    client = APIClient(base_url="https://api.example.com")
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_server_error_raises_exception(mocker):
    """Test that 500 status raises APIGatewayError."""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    # Configure raise_for_status to actually raise an error
    import requests
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    
    mocker.patch('requests.Session.request', return_value=mock_response)
    
    client = APIClient(base_url="https://api.example.com")
    
    with pytest.raises(APIGatewayError) as exc:
        client.get("/error")
    
    assert "500" in str(exc.value.original_exception)
