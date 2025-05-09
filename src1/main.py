from fastapi import FastAPI, Request, WebSocket
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="src1/templates")

app = FastAPI()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
