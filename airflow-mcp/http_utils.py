import requests
from typing import Optional, Dict, Any, Union
from requests.exceptions import RequestException, Timeout, ConnectionError
import json


class HTTPUtils:
    """
    A utility class for making HTTP requests with configurable global settings.
    Each request uses its own session.
    
    Args:
        base_url: Base URL for all requests (optional)
        verify_ssl: Whether to verify SSL certificates (default: True)
        timeout: Default timeout for requests in seconds (default: 30)
        headers: Default headers to include in all requests (optional)
        auth: Authentication tuple (username, password) for all requests (optional)
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[tuple] = None
    ):
        self.base_url = base_url.rstrip('/') if base_url else None
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        
        # Set default headers with Content-Type as application/json
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if headers:
            self.default_headers.update(headers)
            
        self.auth = auth
        
    def _build_url(self, endpoint: str) -> str:
        """Construct full URL from base URL and endpoint."""
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint
        if self.base_url:
            return f"{self.base_url}/{endpoint.lstrip('/')}"
        return endpoint
    
    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge request-specific headers with default headers."""
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged
    
    def make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        body: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with error handling.
        Each request uses its own session.
        
        Args:
            endpoint: API endpoint or full URL
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            body: Request body (dict or string)
            headers: Request-specific headers
            params: URL query parameters
            timeout: Request-specific timeout (overrides default)
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            requests.Response object
            
        Raises:
            requests.exceptions.Timeout: If request times out
            requests.exceptions.ConnectionError: If connection fails
            requests.exceptions.HTTPError: If response status indicates error
            requests.exceptions.RequestException: For other request errors
        """
        url = self._build_url(endpoint)
        merged_headers = self._merge_headers(headers)
        request_timeout = timeout if timeout is not None else self.timeout
        
        try:
            # Prepare request kwargs
            request_kwargs = {
                'verify': self.verify_ssl,
                'timeout': request_timeout,
                'headers': merged_headers,
                'params': params,
                'auth': self.auth,
                **kwargs
            }
            
            # Handle body based on content type
            if body is not None:
                if isinstance(body, dict):
                    if merged_headers.get('Content-Type') == 'application/json':
                        request_kwargs['json'] = body
                    else:
                        request_kwargs['data'] = body
                else:
                    request_kwargs['data'] = body
            
            # Make the request with a new session
            response = requests.request(
                method=method.upper(),
                url=url,
                **request_kwargs
            )
            
            # Raise exception for bad status codes (4xx, 5xx)
            response.raise_for_status()
            
            return response
            
        except Timeout as e:
            raise Timeout(f"Request to {url} timed out after {request_timeout}s") from e
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to {url}") from e
        except requests.exceptions.HTTPError as e:
            # Re-raise with more context
            status_code = e.response.status_code
            try:
                error_body = e.response.text
            except:
                error_body = "Unable to read response body"
            raise requests.exceptions.HTTPError(
                f"HTTP {status_code} error for {url}: {error_body}",
                response=e.response
            ) from e
        except RequestException as e:
            raise RequestException(f"Request to {url} failed: {str(e)}") from e
    
    def get_json_response(
        self,
        endpoint: str,
        method: str = 'GET',
        body: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> Any:
        """
        Make an HTTP request and return JSON response body.
        
        Args:
            endpoint: API endpoint or full URL
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            body: Request body (dict or string)
            headers: Request-specific headers
            params: URL query parameters
            timeout: Request-specific timeout (overrides default)
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Parsed JSON response (dict, list, or other JSON-serializable type)
            
        Raises:
            json.JSONDecodeError: If response body is not valid JSON
            All exceptions from make_request()
        """
        response = self.make_request(
            endpoint=endpoint,
            method=method,
            body=body,
            headers=headers,
            params=params,
            timeout=timeout,
            **kwargs
        )
        
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse JSON response from {response.url}: {e.msg}",
                e.doc,
                e.pos
            ) from e
