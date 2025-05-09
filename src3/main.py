from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="src3/templates")

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: set = set()
        # self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        # self.active_connections.append(websocket)
        print(f"connection list: {self.active_connections}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"connection list: {self.active_connections}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    print(f"ws endpoint headers: {websocket.headers}")
    print(f"ws endpoint query_params: {websocket.query_params}")
    print(f"ws endpoint path_params: {websocket.path_params}")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
