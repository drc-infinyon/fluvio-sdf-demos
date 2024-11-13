import json
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Set
import uuid
from datetime import datetime
import numpy as np

@dataclass
class GameItem:
    item_id: str
    category: str
    name: str
    price: float

@dataclass
class Player:
    player_id: str
    current_level: int
    is_online: bool
    level_advance_probability: float
    purchase_probability: float
    last_level_advance_time: int
    logout_probability: float

@dataclass
class GameServer:
    server_id: str
    is_online: bool
    current_players: Set[str]
    max_capacity: int

class GameSimulator:
    def __init__(self, config_file: str):
        self.config = self.load_config(config_file)
        self.servers: Dict[str, GameServer] = {}
        self.players: Dict[str, Player] = {}
        self.items: Dict[str, GameItem] = {}
        self.current_time = 0
        self.initialize_simulation()

    def load_config(self, config_file: str) -> dict:
        # In practice, load from actual file
        return {
            "event_config": {
                "player_event_factor": 1.5,
                "server_event_factor": 1.1,
                "event_variance": 0.2
            },
            "server_config": {
                "num_servers": 5,
                "max_capacity": 100,
                "online_to_offline_prob": 0.01,
                "offline_to_online_prob": 0.8
            },
            "player_config": {
                "base_login_prob": 0.3,
                "base_logout_prob": 0.1,
                "increased_logout_prob": 0.3,
                "level_advance_prob_range": (0.1, 0.4),
                "purchase_prob_range": (0.05, 0.2),
                "inactive_threshold": 5
            },
            "item_categories": {
                "outfit_skins": {
                    "price_range": (500, 2000),
                    "items": ["Neon Warrior", "Stealth Suit", "Dragon Scale", "Crystal Armor", "Desert Wanderer"]
                },
                "hats": {
                    "price_range": (100, 500),
                    "items": ["Viking Helm", "Wizard Hat", "Crown of Glory", "Space Helmet", "Pirate Cap"]
                },
                "stickers": {
                    "price_range": (50, 200),
                    "items": ["Lucky Star", "Dragon Mark", "Battle Scar", "Victory Badge", "Guild Emblem"]
                },
                "dances": {
                    "price_range": (200, 1000),
                    "items": ["Victory Dance", "Robot Move", "Tribal Dance", "Break Dance", "Power Pose"]
                }
            }
        }

    def initialize_simulation(self):
        # Initialize servers
        for i in range(self.config["server_config"]["num_servers"]):
            server = GameServer(
                server_id=f"server_{i}",
                is_online=random.random() < 0.8,
                current_players=set(),
                max_capacity=self.config["server_config"]["max_capacity"]
            )
            self.servers[server.server_id] = server

        # Initialize items
        for category, details in self.config["item_categories"].items():
            price_range = details["price_range"]
            for item_name in details["items"]:
                item = GameItem(
                    item_id=str(uuid.uuid4()),
                    category=category,
                    name=item_name,
                    price=random.uniform(*price_range)
                )
                self.items[item.item_id] = item

    def create_player(self) -> Player:
        return Player(
            player_id=str(uuid.uuid4()),
            current_level=1,
            is_online=False,
            level_advance_probability=random.uniform(*self.config["player_config"]["level_advance_prob_range"]),
            purchase_probability=random.uniform(*self.config["player_config"]["purchase_prob_range"]),
            last_level_advance_time=0,
            logout_probability=self.config["player_config"]["base_logout_prob"]
        )

    def generate_events(self) -> List[dict]:
        events = []
        self.current_time += 1

        # Server state transitions
        for server in self.servers.values():
            if server.is_online and random.random() < self.config["server_config"]["online_to_offline_prob"]:
                server.is_online = False
                events.append({
                    "timestamp": self.current_time,
                    "event_type": "server_offline",
                    "server_id": server.server_id
                })
                # Force logout all players
                for player_id in server.current_players.copy():
                    self.handle_player_logout(player_id, server.server_id, events)
            elif not server.is_online and random.random() < self.config["server_config"]["offline_to_online_prob"]:
                server.is_online = True
                events.append({
                    "timestamp": self.current_time,
                    "event_type": "server_online",
                    "server_id": server.server_id
                })

        # Player creation (new players joining the game)
        if random.random() < 0.1:  # 10% chance of new player
            player = self.create_player()
            self.players[player.player_id] = player
            events.append({
                "timestamp": self.current_time,
                "event_type": "new_player",
                "player_id": player.player_id
            })

        # Player actions
        for player in self.players.values():
            if not player.is_online:
                # Login attempt
                if random.random() < self.config["player_config"]["base_login_prob"]:
                    self.handle_player_login(player.player_id, events)
            else:
                # Level advancement
                if random.random() < player.level_advance_probability:
                    player.current_level += 1
                    player.last_level_advance_time = self.current_time
                    events.append({
                        "timestamp": self.current_time,
                        "event_type": "level_advance",
                        "player_id": player.player_id,
                        "new_level": player.current_level
                    })

                # Purchase attempt
                if random.random() < player.purchase_probability:
                    item = random.choice(list(self.items.values()))
                    events.append({
                        "timestamp": self.current_time,
                        "event_type": "item_purchase",
                        "player_id": player.player_id,
                        "item_id": item.item_id,
                        "item_name": item.name,
                        "category": item.category,
                        "price": item.price
                    })

                # Check for logout
                time_since_level = self.current_time - player.last_level_advance_time
                if time_since_level > self.config["player_config"]["inactive_threshold"]:
                    player.logout_probability = self.config["player_config"]["increased_logout_prob"]

                if random.random() < player.logout_probability:
                    server_id = next(server_id for server_id, server in self.servers.items()
                                   if player.player_id in server.current_players)
                    self.handle_player_logout(player.player_id, server_id, events)

        return events

    def handle_player_login(self, player_id: str, events: List[dict]):
        player = self.players[player_id]
        # Find available server
        available_servers = [
            server for server in self.servers.values()
            if server.is_online and len(server.current_players) < server.max_capacity
        ]

        if available_servers:
            server = random.choice(available_servers)
            server.current_players.add(player_id)
            player.is_online = True
            player.logout_probability = self.config["player_config"]["base_logout_prob"]
            events.append({
                "timestamp": self.current_time,
                "event_type": "player_login",
                "player_id": player_id,
                "server_id": server.server_id
            })

    def handle_player_logout(self, player_id: str, server_id: str, events: List[dict]):
        player = self.players[player_id]
        server = self.servers[server_id]
        server.current_players.remove(player_id)
        player.is_online = False
        events.append({
            "timestamp": self.current_time,
            "event_type": "player_logout",
            "player_id": player_id,
            "server_id": server_id
        })

    def run_step(self, timesteps: int = 1) -> List[dict]:
        all_events = []

        for _ in range(timesteps):
            # Generate varying number of events based on active players and servers
            num_online_servers = sum(1 for server in self.servers.values() if server.is_online)
            num_online_players = sum(1 for player in self.players.values() if player.is_online)

            # Base number of events scales with online players and servers
            base_events = (num_online_players * self.config["event_config"]["player_event_factor"]) + (num_online_servers * self.config["event_config"]["server_event_factor"])
            num_events = int(random.gauss(base_events, base_events * self.config["event_config"]["event_variance"]))

            for _ in range(max(1, num_events)):
                events = self.generate_events()
                all_events.extend(events)

        return all_events

# Example usage
if __name__ == "__main__":
    simulator = GameSimulator("config.json")
    events = simulator.run_step()
    print(json.dumps(events, indent=2))

    print("Step 2")
    events = simulator.run_step()
    print(json.dumps(events, indent=2))

    print("Step 3")
    events = simulator.run_step()
    print(json.dumps(events, indent=2))
