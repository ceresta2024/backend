from app.sockets import sio_server


@sio_server.event
async def connect(sid, environ, auth):
    print(f"{sid}: connected")
    await sio_server.emit("join", {"sid": sid})


@sio_server.event
async def message(sid, message):
    await sio_server.emit("message", {"sid": sid, "message": message})


@sio_server.event
async def disconnect(sid):
    print(f"{sid}: disconnected")
