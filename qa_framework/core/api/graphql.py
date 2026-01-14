from typing import Any, Dict, Optional
from qa_framework.core.api.client import APIClient

class GraphQLClient(APIClient):
    """
    Client for GraphQL requests.
    """
    def execute(self, query: str, variables: Optional[Dict[str, Any]] = None, endpoint: str = "/graphql", **kwargs):
        """
        Executes a GraphQL query/mutation.
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
            
        return self.post(endpoint, json_body=payload, **kwargs)
