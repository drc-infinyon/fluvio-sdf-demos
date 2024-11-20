# Gaming Analytics DataFlow

The gaming analytics demo includes the following use cases:

**Player Engagement:** Tracking active players and monitoring engagement across levels and maps to identify where players may get stuck or disengage.

---

## Event Generation

The `data-generator` directory contains two forms of data generation capability: 
- An event generator script using the Fluvio Python client to generate events and produce them to topics.
- A web API wrapper that produces the same data, collected via the HTTP source connector.

### Player Event
This event captures player actions within a game, such as movement, interactions, or level completion, and is sent to the `player-events` topic.

**Schema:**
- **event_name**: Descriptive name for the player action (e.g., `player_action`).
- **parameters**:
  - **player_id**: Unique identifier for the player.
  - **session_id**: Unique identifier for the player's session.
  - **event_type**: Type of event (e.g., `move`, `interaction`, `level_complete`).
  - **level_id**: The game level where the event occurred.
  - **map_id**: The specific map within the level.
- **event_timestamp**: ISO timestamp of the event.
- **user_data**:
  - **user_id**: Consistent player identifier.
  - **platform**: Player’s platform (e.g., `PC`, `Console`).

**Example:**
```json
{
  "event_name": "player_action",
  "parameters": {
    "player_id": "player_123",
    "session_id": "session_456",
    "event_type": "move",
    "level_id": "level_02",
    "map_id": "map_03"
  },
  "event_timestamp": "2024-11-12T10:15:30Z",
  "user_data": {
    "user_id": "player_123",
    "platform": "PC"
  }
}
```

### Purchase (Transaction) Event
This event represents an in-game purchase, which may be subject to fraud analysis, and is sent to the `purchase-events` topic.

**Schema:**
- **event_name**: Standardized name for transaction events (e.g., `transaction`).
- **parameters**:
  - **transaction_id**: Unique identifier for the transaction.
  - **transaction_type**: Type of transaction (e.g., `purchase`, `refund`).
  - **currency**: Currency in which the purchase was made.
  - **amount**: Cost of the item.
  - **item_id**: Identifier of the purchased item (e.g., in-game skin or weapon).
  - **item_type**: Item category (e.g., `skin`, `weapon`).
- **event_timestamp**: ISO timestamp of the purchase.
- **user_data**:
  - **user_id**: Player identifier.
  - **platform**: Player’s platform (e.g., `PC`, `Console`).

**Example:**
```json
{
  "event_name": "transaction",
  "parameters": {
    "transaction_id": "trans_789",
    "transaction_type": "purchase",
    "currency": "USD",
    "amount": 4.99,
    "item_id": "skin_dragon",
    "item_type": "skin"
  },
  "event_timestamp": "2024-11-12T10:16:05Z",
  "user_data": {
    "user_id": "player_123",
    "platform": "PC"
  }
}
```

### Server Metric Event
This event provides server metrics, such as CPU load, memory usage, and latency, essential for monitoring server health, and is sent to the `server-metrics` topic.

**Schema:**
- **event_name**: Name for server metric events (e.g., `server_metric`).
- **parameters**:
  - **server_id**: Unique identifier for the server.
  - **cpu_load**: Current CPU usage as a percentage.
  - **memory_usage**: Current memory usage as a percentage.
  - **latency**: Current network latency in milliseconds.
- **event_timestamp**: ISO timestamp of the server metrics capture.
- **server_data**:
  - **region**: Location or region of the server (e.g., `us-west`).
  - **server_type**: Type of server (e.g., `dedicated`, `virtual`).

**Example:**
```json
{
  "event_name": "server_metric",
  "parameters": {
    "server_id": "server_1",
    "cpu_load": 78,
    "memory_usage": 65,
    "latency": 120
  },
  "event_timestamp": "2024-11-12T10:16:30Z",
  "server_data": {
    "region": "us-west",
    "server_type": "dedicated"
  }
}
```

## To run the app

Install Docker

Navigate to the directory

Run 'make start' or 'docker compose up --detach'

## 

---

