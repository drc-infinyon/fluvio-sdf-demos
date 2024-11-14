
`cargo run` to start the server. The server uses a fluvio client to access
topic data from a websocket enpoint ws://127.0.0.1:3001/ws/TOPIC_NAME

Visit http://localhost:3001

Static html pages can render data from any topic by visiting the endpoint

see `static/table.html` for an example.
