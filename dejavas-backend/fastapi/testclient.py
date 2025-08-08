from typing import Any, Dict
from . import HTTPException

__all__ = ["TestClient"]


class Response:
    def __init__(self, status_code: int, content: Any) -> None:
        self.status_code = status_code
        self._content = content

    def json(self) -> Any:
        return self._content


class TestClient:
    def __init__(self, app: Any) -> None:
        self.app = app

    def post(self, path: str, json: Dict[str, Any] | None = None) -> Response:
        try:
            result = self.app._call("POST", path, json)
            if hasattr(result, "dict"):
                result = result.dict()
            return Response(200, result)
        except HTTPException as exc:  # type: ignore[misc]
            return Response(exc.status_code, {"detail": exc.detail})

    def get(self, path: str) -> Response:
        try:
            result = self.app._call("GET", path)
            if hasattr(result, "dict"):
                result = result.dict()
            return Response(200, result)
        except HTTPException as exc:  # type: ignore[misc]
            return Response(exc.status_code, {"detail": exc.detail})
