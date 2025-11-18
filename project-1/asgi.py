from app.main import api  # absolute import from your app package

app = api  # uv expects the ASGI app object to be named 'app'
