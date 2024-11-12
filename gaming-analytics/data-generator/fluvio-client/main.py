import random
import time
from datetime import datetime
from fluvio import Fluvio, FluvioError

# Initialize the Fluvio client
fluvio = Fluvio()

# Define sample data templates
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
maps = ["map_01", "map_02", "map_03"]
levels = ["level_01", "level_02", "level_03"]
servers = ["server_1", "server_2", "server_3"]

# Function to generate player events
def generate_player_event():
    return {
        "player_id": random.choice(player_ids),
        "session_id": f"session_{random.randint(1000, 9999)}",
        "event_type": random.choice(["move", "interaction", "level_complete"]),
        "level_id": random.choice(levels),
        "map_id": random.choice(maps),
        "timestamp": datetime.utcnow().isoformat()
    }

# Function to generate purchase events
def generate_purchase_event():
    return {
        "player_id": random.choice(player_ids),
        "item_id": random.choice(items),
        "price": round(random.uniform(0.99, 29.99), 2),
        "currency": "USD",
        "purchase_timestamp": datetime.utcnow().isoformat(),
        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    }

# Function to generate server metric events
def generate_server_metric():
    return {
        "server_id": random.choice(servers),
        "cpu_load": random.randint(20, 100),
        "memory_usage": random.randint(30, 90),
        "latency": random.randint(50, 300),
        "timestamp": datetime.utcnow().isoformat()
    }

# Publish events to Fluvio topics
def publish_events():
    try:
        player_topic = fluvio.topic_producer("player_events")
        purchase_topic = fluvio.topic_producer("purchases")
        server_topic = fluvio.topic_producer("server_metrics")
        
        while True:
            player_event = generate_player_event()
            purchase_event = generate_purchase_event()
            server_metric = generate_server_metric()
            
            player_topic.send("player_events", str(player_event))
            player_topic.flush()
            purchase_topic.send("purchases", str(purchase_event))
            purchase_topic.flush()
            server_topic.send("server_metrics", str(server_metric))
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
