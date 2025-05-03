from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from src.helper import env_load_helper
import os
import importlib
from src.middleware import api_middleware
from src.helper import check_helper
from fastapi.middleware.cors import CORSMiddleware

class ApiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/api"):
            token = request.headers.get("Authorization")
            api_middleware.verify_token(request, token)
        
        response = await call_next(request)
        return response
    
app = FastAPI()

origins = ["*", 'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ApiMiddleware)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=400,  
        content={"code": 400, "respond": str(exc)} 
    )

dir = os.listdir("src/router")

for filename in dir:
    module_name = f"src.router.{filename[:-3]}"
    module = importlib.import_module(module_name)
    app.include_router(module.router)

    print(f"Đã nạp router từ {module_name}")

if __name__ == "__main__":
    try:
        check_helper.check_everything_before_start_socket()
        env_load_helper.load_env()
        uvicorn.run(app, host="127.0.0.1", port= int(os.getenv('SERVER_PORT')))
    except Exception as e:
        print(str(e))

