import re
import inspect
from typing import Any, Callable, Dict, List, Tuple
from pydantic import BaseModel

__all__ = ["FastAPI", "HTTPException"]


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class FastAPI:
    def __init__(self) -> None:
        self._routes: Dict[str, List[Tuple[re.Pattern[str], Callable[..., Any]]]] = {
            "GET": [],
            "POST": [],
        }

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self._add_route("GET", path)

    def post(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self._add_route("POST", path)

    def _add_route(self, method: str, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        pattern = self._compile_path(path)

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._routes[method].append((pattern, func))
            return func

        return decorator

    @staticmethod
    def _compile_path(path: str) -> re.Pattern[str]:
        regex = re.sub(r"{([^}]+)}", r"(?P<\1>[^/]+)", path.rstrip("/"))
        regex = f"^{regex}/?$"
        return re.compile(regex)

    def _call(self, method: str, path: str, json: Any = None) -> Any:
        path = path.rstrip("/")
        for pattern, func in self._routes.get(method, []):
            match = pattern.match(path)
            if not match:
                continue
            params = match.groupdict()
            kwargs: Dict[str, Any] = {}
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                if name in params:
                    kwargs[name] = params[name]
                elif json is not None and param.annotation is not inspect._empty:
                    ann = param.annotation
                    if isinstance(ann, type) and issubclass(ann, BaseModel):
                        kwargs[name] = ann.parse_obj(json)
                    else:
                        kwargs[name] = json
            return func(**kwargs)
        raise HTTPException(status_code=404, detail="Session not found")

    # --- Minimal development server -------------------------------------------------
    def serve(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Run a very small HTTP server for manual testing.

        This helper exists so the application can be tried in environments
        where real FastAPI/Uvicorn packages are unavailable.  It is intentionally
        lightweight and only supports the subset of functionality required by
        the demo endpoints used in the tests.
        """
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import json

        app = self

        class Handler(BaseHTTPRequestHandler):
            def _dispatch(self, method: str) -> None:
                try:
                    length = int(self.headers.get("Content-Length", 0)) if method == "POST" else 0
                    body = self.rfile.read(length) if length else b""
                    payload = json.loads(body.decode() or "{}") if body else None
                    result = app._call(method, self.path, payload)
                    if hasattr(result, "dict"):
                        result = result.dict()
                    content = json.dumps(result).encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                except HTTPException as exc:  # type: ignore[misc]
                    content = json.dumps({"detail": exc.detail}).encode()
                    self.send_response(exc.status_code)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)

            def do_GET(self) -> None:  # pragma: no cover - manual use only
                self._dispatch("GET")

            def do_POST(self) -> None:  # pragma: no cover - manual use only
                self._dispatch("POST")

        server = HTTPServer((host, port), Handler)
        try:  # pragma: no cover - manual use only
            print(f"Serving on http://{host}:{port}")
            server.serve_forever()
        finally:  # pragma: no cover - manual use only
            server.server_close()
