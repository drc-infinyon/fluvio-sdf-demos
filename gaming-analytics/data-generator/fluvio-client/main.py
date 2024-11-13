import random
import time
from datetime import datetime
from fluvio import Fluvio, FluvioError

# Initialize the Fluvio client
fluvio = Fluvio()

# Sample data templates
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
maps = ["map_01", "map_02", "map_03"]
levels = ["level_01", "level_02", "level_03"]
servers = ["server_1", "server_2", "server_3"]
platforms = ["PC", "Console"]

# Function to generate player event
def generate_player_event():
    return {
        "event_name": "player_action",
        "parameters": {
            "player_id": random.choice(player_ids),
            "session_id": f"session_{random.randint(1000, 9999)}",
            "event_type": random.choice(["move", "interaction", "level_complete"]),
            "level_id": random.choice(levels),
            "map_id": random.choice(maps)
        },
        "event_timestamp": datetime.utcnow().isoformat(),
        "user_data": {
            "user_id": random.choice(player_ids),
            "platform": random.choice(platforms)
        }
    }

# Function to generate transaction event
def generate_purchase_event():
    return {
        "event_name": "transaction",
        "parameters": {
            "transaction_id": f"trans_{random.randint(1000, 9999)}",
            "transaction_type": "purchase",
            "currency": "USD",
            "amount": round(random.uniform(0.99, 29.99), 2),
            "item_id": random.choice(items),
            "item_type": "skin"
        },
        "event_timestamp": datetime.utcnow().isoformat(),
        "user_data": {
            "user_id": random.choice(player_ids),
            "platform": random.choice(platforms)
        }
    }

# Function to generate server metric event
def generate_server_metric():
    return {
        "event_name": "server_metric",
        "parameters": {
            "server_id": random.choice(servers),
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

# Publish events to Fluvio topics
def publish_events():
    try:
        player_topic = fluvio.topic_producer("player-events")
        purchase_topic = fluvio.topic_producer("purchase-events")
        server_topic = fluvio.topic_producer("server-metrics")
        
        while True:
            player_event = generate_player_event()
            purchase_event = generate_purchase_event()
            server_metric = generate_server_metric()
            
            player_topic.send("player-events", str(player_event))
            player_topic.flush()
            purchase_topic.send("purchase-events", str(purchase_event))
            purchase_topic.flush()
            server_topic.send("server-metrics", str(server_metric))
            server_topic.flush()
            
            print(f"Sent player event: {player_event}")
            print(f"Sent purchase event: {purchase_event}")
            print(f"Sent server metric: {server_metric}")
            
            time.sleep(1 / 100)  # Generate 100 events per second

    except FluvioError as e:
        print(f"Fluvio Error: {e}")

# Run the data generator
if __name__ == "__main__":
    publish_events()
