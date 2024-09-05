import socketio

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")
    # sio.emit('new_notification', {'user_id': '66d6aaeaf19629a103105353', 'message': 'Testing from client'})

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.on('new_notification')
def new_notification(data):
    print(f"New notification: {data}")


# Connect to the Socket.IO server
sio.connect(
    "http://127.0.0.1:5006",  # Connect to the server base URL
    headers={
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mbyI6eyJpZCI6Ik5qWmtObUZoWldGbU1UazJNamxoTVRBek1UQTFNelV6IiwiZmlyc3RfbmFtZSI6IkFydW4iLCJsYXN0X25hbWUiOiJNb25kYWwiLCJwZXJtaXNzaW9uS2V5IjoicGVybWl0X05qWmtObUZoWldGbU1UazJNamxoTVRBek1UQTFNelV6In0sImV4cCI6MTcyNzkzNjgyMH0.Goez1cDrkzLsCNAn4KSYr1fzW3-opGzmdGOL0S8zRpU"
    },
)



# Wait for some time to receive messages
sio.wait()
