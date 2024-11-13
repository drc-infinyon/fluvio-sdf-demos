# Gaming Analytics DataFlow

The gaming analytics demo includes the following use cases:

**Player Engagement:** Tracking active players and monitoring engagement across levels and maps to identify where players may get stuck or disengage.

**Purchase Behavior & Fraud Detection:** Real-time analytics on in-game purchases to understand item popularity and flag potential fraud.

**Server Health:** Monitoring server performance to maintain high-quality gameplay.

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

---

## Step-by-Step Fluvio Client

### Prerequisites
Ensure Fluvio is installed and running. You can follow the [Fluvio Quickstart Guide](https://www.fluvio.io/docs/getting-started/).

### Create Topics
Create the necessary Fluvio topics: `player-events`, `purchase-events`, and `server-metrics` by running the following commands:

```bash
fluvio topic create player-events
fluvio topic create purchase-events
fluvio topic create server-metrics
```

### Running the Data Generator

1. **Navigate to the `data-generator/fluvio-client` Directory:**

   ```bash
   cd path/to/gaming-analytics/data-generator/fluvio-client
   ```

2. **Set Up a Virtual Environment (Optional but recommended):**

   ```bash
   python3 -m venv gaming-analytics
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   Install the Fluvio client library from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Data Generator:**

   Start the data generator by running `main.py`, which will begin producing events to the specified Fluvio topics:

   ```bash
   python main.py
   ```

   This script will:
   - Generate synthetic data for **player events**, **purchase events**, and **server metric events**.
   - Publish each event to its corresponding Fluvio topic (`player-events`, `purchase-events`, and `server-metrics`).
   - Print each event to the console as it is produced.

5. **Verify Data in Fluvio Topics:**

   Use the following commands to verify that data is being produced to each topic:

   ```bash
   fluvio consume player-events -B
   fluvio consume purchase-events -B
   fluvio consume server-metrics -B
   ```

   The `-B` flag consumes all messages in the topic from the beginning, allowing you to see the events produced by `main.py`.

### Stopping the Data Generator
To stop the data generator, simply press `Ctrl+C` in the terminal where `main.py` is running.

## Step-by-Step HTTP API

**Run the API**
Start the API server with Uvicorn:

```bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
```
The server will now listen on http://localhost:8000 (or the specified host and port). You can access each event generator by navigating to the endpoints:

Player Event: http://localhost:8000/player_event
Purchase Event: http://localhost:8000/purchase_event
Server Metric: http://localhost:8000/server_metric

EVents are streamed in real-time here: http http://localhost:8000/stream_events

**Connect with Fluvio HTTP Connector**

To integrate this API with Fluvio, configure the Fluvio HTTP connector to point to these endpoints. The connector will then fetch events as needed, enabling real-time ingestion of the generated data.




-----
#   player-event:
#     type: object
#     properties:
#       event_name:
#         type: string
#       parameters:
#        type: player-event-parameters
#       event_timestamp:
#         type: string
#       user_data:
#         type: object
#         properties:
#           user_id:
#             type: string
#           platform:
#             type: string

#   purchase-event:
#     type: object
#     properties:
#       event_name:
#         type: string
#       parameters:
#         type: object
#         properties:
#           transaction_id:
#             type: string
#           transaction_type:
#             type: string
#           currency:
#             type: string
#           amount:
#             type: f64
#           item_id:
#             type: string
#           item_type:
#             type: string
#       event_timestamp:
#         type: string
#       user_data:
#         type: object
#         properties:
#           user_id:
#             type: string
#           platform:
#             type: string

#   server-metric:
#     type: object
#     properties:
#       event_name:
#         type: string
#       parameters:
#         type: object
#         properties:
#           server_id:
#             type: string
#           cpu_load:
#             type: u32
#           memory_usage:
#             type: u32
#           latency:
#             type: u32
#       event_timestamp:
#         type: string
#       server_data:
#         type: object
#         properties:
#           region:
#             type: string
#           server_type:
#             type: string

# topics:
#   player-events:
#     schema:
#       value:
#         type: player-event
  
#   purchase-events:
#     schema:
#       value:
#         type: purchase-event
  
#   server-metrics:
#     schema:
#       value:
#         type: server-metric

# services:
#   # Monitor player sessions
#   player-session-analytics:
#     sources:
#       - type: topic
#         id: player-events
#     transforms:
#       - operator: map
#         run: |
#           fn analyze_player_session(event: PlayerEvent) -> Result<PlayerSessionSummary> {
#             // Implement your logic to summarize player sessions
#             Ok(PlayerSessionSummary {
#               player_id: event.parameters.player_id.clone(),
#               event_count: 1,  // Example placeholder
#             })
#           }
#     sinks:
#       - type: topic
#         id: player-session-summaries

#   # Aggregate purchases
#   purchase-aggregator:
#     sources:
#       - type: topic
#         id: purchase-events

#     transforms:
#       - operator: map
#         run: |
#           fn aggregate_purchases(event: PurchaseEvent) -> Result<PurchaseAggregation> {
#             let mut aggregation = purchase_aggregation().get_or_default(&event.user_data.user_id);

#             // Update the aggregation state
#             aggregation.total_amount += event.parameters.amount;
#             aggregation.transaction_count += 1;

#             Ok(aggregation)
#           }
#     sinks:
#       - type: topic
#         id: purchase-aggregates

#   # Monitor server health
#   server-health-monitor:
#     sources:
#       - type: topic
#         id: server-metrics
#     transforms:
#       - operator: filter
#         run: |
#           fn is_server_overloaded(metric: ServerMetric) -> Result<bool> {
#             Ok(metric.parameters.cpu_load > 80 || metric.parameters.memory_usage > 80)
#           }
#     sinks:
#       - type: topic
#         id: server-alerts

#   # Detect fraudulent transactions
#   fraud-detection:
#     sources:
#       - type: topic
#         id: purchase-events

#     transforms:
#       - operator: flat-map
#         run: |
#           fn detect_fraud(event: PurchaseEvent) -> Result<Option<FraudAlert>> {
#             let user_id = event.user_data.user_id.clone();
#             let mut stats = user_purchase_stats().get_or_default(&user_id);

#             // Update transaction count and currency list
#             stats.transaction_count += 1;
#             if !stats.currencies.contains(&event.parameters.currency) {
#               stats.currencies.push(event.parameters.currency.clone());
#             }

#             // Define fraud criteria
#             let is_frequent = stats.transaction_count > 5; // Example threshold
#             let is_multi_currency = stats.currencies.len() > 1;

#             // Return fraud alert if criteria are met
#             if is_frequent || is_multi_currency {
#               Ok(Some(FraudAlert {
#                 user_id,
#                 reason: if is_frequent {
#                   "Too frequent transactions".to_string()
#                 } else {
#                   "Multiple currency transactions".to_string()
#                 },
#               }))
#             } else {
#               Ok(None)
#             }
#           }
#     sinks:
#       - type: topic
#         id: fraud-alerts
