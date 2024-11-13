from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime
from typing import Dict

app = FastAPI()

# Sample data templates
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
maps = ["map_01", "map_02", "map_03"]
levels = ["level_01", "level_02", "level_03"]
servers = ["server_1", "server_2", "server_3"]
platforms = ["PC", "Console"]

class PlayerEvent(BaseModel):
    event_name: str = "player_action"
    parameters: Dict[str, str]
    event_timestamp: str
    user_data: Dict[str, str]

class PurchaseEvent(BaseModel):
    event_name: str = "transaction"
    parameters: Dict[str, str]
    event_timestamp: str
    user_data: Dict[str, str]

class ServerMetric(BaseModel):
    event_name: str = "server_metric"
    parameters: Dict[str, int]
    event_timestamp: str
    server_data: Dict[str, str]

def generate_player_event() -> Dict:
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

def generate_purchase_event() -> Dict:
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

def generate_server_metric() -> Dict:
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

@app.get("/player_event", response_model=PlayerEvent)
async def get_player_event():
    return generate_player_event()

@app.get("/purchase_event", response_model=PurchaseEvent)
async def get_purchase_event():
    return generate_purchase_event()

@app.get("/server_metric", response_model=ServerMetric)
async def get_server_metric():
    return generate_server_metric()
