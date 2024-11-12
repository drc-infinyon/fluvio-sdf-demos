from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime
from typing import Dict

app = FastAPI()

# Sample data for generating synthetic events
player_ids = [f"player_{i}" for i in range(1, 100)]
items = ["sword", "shield", "potion", "armor", "skin_dragon", "skin_phoenix"]
maps = ["map_01", "map_02", "map_03"]
levels = ["level_01", "level_02", "level_03"]
servers = ["server_1", "server_2", "server_3"]

class PlayerEvent(BaseModel):
    player_id: str
    session_id: str
    event_type: str
    level_id: str
    map_id: str
    timestamp: str

class PurchaseEvent(BaseModel):
    player_id: str
    item_id: str
    price: float
    currency: str
    purchase_timestamp: str
    ip_address: str

class ServerMetric(BaseModel):
    server_id: str
    cpu_load: int
    memory_usage: int
    latency: int
    timestamp: str

def generate_player_event() -> Dict:
    return {
        "player_id": random.choice(player_ids),
        "session_id": f"session_{random.randint(1000, 9999)}",
        "event_type": random.choice(["move", "interaction", "level_complete"]),
        "level_id": random.choice(levels),
        "map_id": random.choice(maps),
        "timestamp": datetime.utcnow().isoformat()
    }

def generate_purchase_event() -> Dict:
    return {
        "player_id": random.choice(player_ids),
        "item_id": random.choice(items),
        "price": round(random.uniform(0.99, 29.99), 2),
        "currency": "USD",
        "purchase_timestamp": datetime.utcnow().isoformat(),
        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    }

def generate_server_metric() -> Dict:
    return {
        "server_id": random.choice(servers),
        "cpu_load": random.randint(20, 100),
        "memory_usage": random.randint(30, 90),
        "latency": random.randint(50, 300),
        "timestamp": datetime.utcnow().isoformat()
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
