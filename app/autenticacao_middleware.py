from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationToken(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_path = request.url.path

        # Adicione o caminho da API de criação de usuários aqui
        if (
            request_path.startswith("/login") or 
            request_path.startswith("/usuarios/criar") or # LIBERADO
            request_path.startswith("/static") or
            request_path.startswith("/docs") or 
            request_path.startswith("/openapi.json")
        ):
            return await call_next(request)
        
        token = request.cookies.get("session_token")

        if token != 'token-senha':
            return RedirectResponse(url="/login", status_code=303)

        return await call_next(request)