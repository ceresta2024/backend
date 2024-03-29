import socketio

# create a Socket.IO server
sio_server = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[],
    # cors_allowed_origins='*'
)

sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="sockets")
