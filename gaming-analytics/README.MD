# Gaming Analytics DataFlow

The gaming analytics demo includes the following use cases:

**Player Engagement:** Tracking active players and monitoring engagement across levels and maps to identify where players may get stuck or disengage.

**Purchase Behavior & Fraud Detection:** Real-time analytics on in-game purchases to understand item popularity and flag potential fraud.

**Server Health:** Monitoring server performance to maintain high-quality gameplay.



## Event Generation

The data generator directory contains two forms of data generation capability. An event generator script using the Flvio Pthon client to generate events and produce to topics, and a web API wrapper that produces the same data that is collected using the HTTP source connector.


### Player Event

This event captures player actions within a game, such as movement, interactions, or level completion. This event is sent to `player-events` topic.

- player_id: Unique identifier for the player.
- session_id: Unique identifier for the player's session.
- event_type: Type of event (e.g., move, interaction, level_complete).
- level_id: The game level where the event occurred.
- map_id: The specific map within the level.
- timestamp: ISO timestamp of the event.

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

This connector sends events to `cars` topic.

### License Plates Connector

The second connector reads car licenses every hour to emulate a database read of license places from an official organization such as the Department of Motor Vehicles (DMV).


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

The connector sends events to `licenses` topic.

## Step-by-step

Take a look at the [dataflow.yaml](./dataflow.yaml) to get an idea of what we're doing.