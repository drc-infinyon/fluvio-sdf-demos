import random
import time
from datetime import datetime
from fluvio import Fluvio
import json

# Connect to the Fluvio client
fluvio = Fluvio.connect()

# Sample data templates
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
item_weights = [0.1, 0.1, 0.2, 0.15, 0.21, 0.18]
maps = ["map_01", "map_02", "map_03"]
levels = ["level_01", "level_02", "level_03"]
servers = ["server_1", "server_2", "server_3"]
platforms = ["PC", "Console"]

# Function to generate player event
def generate_player_event():
    player_id = random.choice(player_ids)
    return {
        "key": player_id,
        "event": {
            "event_name": "player_action",
            "parameters": {
                "player_id": player_id,
                "session_id": f"session_{random.randint(1000, 9999)}",
                "event_type": random.choice(["move", "interaction", "level_complete"]),
                "level_id": random.choice(levels),
                "map_id": random.choice(maps)
            },
            "event_timestamp": datetime.utcnow().isoformat(),
            "user_data": {
                "user_id": player_id,
                "platform": random.choice(platforms)
            }
        }
    }

# Function to generate purchase event
def generate_purchase_event():
    transaction_id = f"trans_{random.randint(1000, 9999)}"
    player_id = random.choice(player_ids)

    return {
        "key": transaction_id,
        "event": {
            "event_name": "transaction",
            "parameters": {
                "transaction_id": transaction_id,
                "transaction_type": "purchase",
                "currency": "USD",
                "amount": round(random.uniform(0.99, 29.99), 2),
                "item_id": random.choices(items, weights=item_weights, k=1)[0],
                "item_type": "skin"
            },
            "event_timestamp": datetime.utcnow().isoformat(),
            "user_data": {
                "user_id": player_id,
                "platform": random.choice(platforms)
            }
        }
    }

# Function to generate server metric event
def generate_server_metric():
    server_id = random.choice(servers)
    return {
        "key": server_id,
        "event": {
            "event_name": "server_metric",
            "parameters": {
                "server_id": server_id,
                "cpu_load": random.randint(20, 100),
                "memory_usage": random.randint(30, 90),
                "latency": random.randint(50, 300)
            },
            "event_timestamp": datetime.utcnow().isoformat(),
            "server_data": {
                "region": "us-west",
                "server_type": "dedicated"
            }
        }
    }

# Publish events to Fluvio topics
def publish_events():
    try:
        # Producers for each topic
        player_topic = fluvio.topic_producer("player-events")
        purchase_topic = fluvio.topic_producer("purchase-events")
        server_topic = fluvio.topic_producer("server-metrics")

        while True:
            # Generate events
            player_event_data = generate_player_event()
            purchase_event_data = generate_purchase_event()
            server_metric_data = generate_server_metric()

            # Encode key and event as UTF-8 bytes
            player_topic.send(player_event_data["key"].encode("utf-8"), json.dumps(player_event_data["event"]).encode("utf-8"))
            player_topic.flush()

            purchase_topic.send(purchase_event_data["key"].encode("utf-8"), json.dumps(purchase_event_data["event"]).encode("utf-8"))
            purchase_topic.flush()

            server_topic.send(server_metric_data["key"].encode("utf-8"), json.dumps(server_metric_data["event"]).encode("utf-8"))
            server_topic.flush()

            print(f"Sent player event: {player_event_data}")
            print(f"Sent purchase event: {purchase_event_data}")
            print(f"Sent server metric: {server_metric_data}")

            time.sleep(1 / 100)  # Generate 100 events per second

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the data generator
if __name__ == "__main__":
    publish_events()
