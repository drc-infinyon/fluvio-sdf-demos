# Gaming Analytics DataFlow

The gaming analytics demo includes the following use cases:

**Player Engagement:** Tracking active players and monitoring engagement across levels and maps to identify where players may get stuck or disengage.

**Purchase Behavior & Fraud Detection:** Real-time analytics on in-game purchases to understand item popularity and flag potential fraud.

**Server Health:** Monitoring server performance to maintain high-quality gameplay.



## Event Generation

The data generator directory contains two forms of data generation capability. An event generator script using the Fluvio Python client to generate events and produce to topics, and a web API wrapper that produces the same data that is collected using the HTTP source connector.


### Player Event
This event captures player actions within a game, such as movement, interactions, or level completion. This event is sent to `player-events` topic.

**Schema:**
- player_id: Unique identifier for the player.
- session_id: Unique identifier for the player's session.
- event_type: Type of event (e.g., move, interaction, level_complete).
- level_id: The game level where the event occurred.
- map_id: The specific map within the level.
- timestamp: ISO timestamp of the event.

**Example:**
```json
{
  "player_id": "player_123",
  "session_id": "session_456",
  "event_type": "move",          // Options: "move", "interaction", "level_complete"
  "level_id": "level_02",
  "map_id": "map_03",
  "timestamp": "2024-11-12T10:15:30Z"
}
```

### Purchase Event
This event represents an in-game purchase made by a player, which may be subject to fraud analysis. This event is sent to `purchase-events` topic.

**Schema:**
- player_id: Unique identifier for the player making the purchase.
- item_id: Identifier of the purchased item (e.g., in-game skin or weapon).
- price: Cost of the item.
- currency: Currency in which the purchase was made.
- purchase_timestamp: ISO timestamp of the purchase.
- ip_address: IP address of the player, which could be used in fraud detection.

**Example:**
```json
{
  "player_id": "player_123",
  "item_id": "skin_dragon",
  "price": 4.99,
  "currency": "USD",
  "purchase_timestamp": "2024-11-12T10:16:05Z",
  "ip_address": "192.168.1.100"
}
```

### Server Metric Event
This event provides server metrics, such as CPU load, memory usage, and latency, essential for monitoring server health. This event is sent to `server-metrics` topic.

**Schema:**
- server_id: Unique identifier for the server.
- cpu_load: Current CPU usage as a percentage.
- memory_usage: Current memory usage as a percentage.
- latency: Current network latency in milliseconds.
- timestamp: ISO timestamp of the server metrics capture.

**Example:**
```json
{
  "server_id": "server_1",
  "cpu_load": 78,              // CPU load percentage
  "memory_usage": 65,          // Memory usage percentage
  "latency": 120,              // Latency in milliseconds
  "timestamp": "2024-11-12T10:16:30Z"
}
```

## Step-by-step

**Prerequisites**
Make sure Fluvio is installed and running. You can follow [Fluvio Quickstart].

**Create Topics**
Create the Fluvio topics - player-events, purchase-events, server-metrics).

Run the following commands to create these topics:

```bash
fluvio topic create player-events
fluvio topic create purchase-events
fluvio topic create server-metrics
```
Navigate to the data-generator/fluvio-client Directory:

```bash
cd ./data-generator/fluvio-client
```

Set Up a Virtual Environment (Optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies**

If you haven’t already, install the Fluvio client library from requirements.txt:

```bash
pip install -r requirements.txt
```
**Run the Data Generator**
Start the data generator by running main.py, which will begin producing events to the specified Fluvio topics:

```bash
python main.py
```

This script will generate synthetic data for player events, purchase events, and server metric events.
Publish each event to its corresponding Fluvio topic (player-events, purchase-events, and server-metrics).

Print each event to the console as it is produced.

**Verify Data in Fluvio Topics**
Use the following commands to verify that data is being produced to each topic.

```bash
fluvio consume player-events -B
fluvio consume purchase-events -B
fluvio consume server-metrics -B
```

The -B flag consumes all messages in the topic from the beginning, allowing you to see the events produced by main.py.

**Stopping the Data Generator**
To stop the data generator, simply press Ctrl+C in the terminal where main.py is running.





[Fluvio Quickstart]