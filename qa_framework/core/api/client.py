import requests
import json
from typing import Any, Dict, Optional
from qa_framework.core.logger import get_logger
from qa_framework.core.exceptions import APIGatewayError

logger = get_logger("api_client")

class APIClient:
    """
    Generic API Client using requests.
    """
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.session = requests.Session()

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"API Request: {method} {url}", **kwargs)

    def _log_response(self, response: requests.Response):
        try:
            body = response.json()
        except ValueError:
            body = response.text
        logger.info(f"API Response: {response.status_code}", body=body)

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        
        self._log_request(method, url, **kwargs)
        
        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request Failed: {str(e)}")
            raise APIGatewayError(f"API Request {method} {url} failed", original_exception=e)

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Any = None, json_body: Any = None, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, data=data, json=json_body, **kwargs)

    def put(self, endpoint: str, data: Any = None, json_body: Any = None, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, data=data, json=json_body, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)
