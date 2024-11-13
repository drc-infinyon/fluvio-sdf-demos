from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime
import json

app = FastAPI()

# Sample data templates
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
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
                "item_id": random.choice(items),
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

# Define endpoints
@app.get("/player_event")
async def player_event():
    event = generate_player_event()
    return {"key": event["key"], "event": event["event"]}

@app.get("/purchase_event")
async def purchase_event():
    event = generate_purchase_event()
    return {"key": event["key"], "event": event["event"]}

@app.get("/server_metric")
async def server_metric():
    event = generate_server_metric()
    return {"key": event["key"], "event": event["event"]}

