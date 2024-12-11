import json
import logging
import os
import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Any


class ServerState(Enum):
    ONLINE = auto()
    OFFLINE = auto()
    MAINTENANCE = auto()


class PlayerState(Enum):
    LOGGED_IN = auto()
    IN_GAME = auto()
    IDLE = auto()
    OFFLINE = auto()


@dataclass
class MapLevel:
    map_name: str
    level_number: int
    difficulty_array: List[float]

    def get_current_difficulty(self) -> float:
        """
        Retrieve difficulty for the current level.
        If level exceeds array, return the last difficulty value.
        """
        return self.difficulty_array[
            min(self.level_number - 1, len(self.difficulty_array) - 1)
        ]


@dataclass
class Player:
    player_id: str
    skill_level: float
    current_map: str = None
    current_level: int = 1
    state: PlayerState = PlayerState.OFFLINE
    deaths: int = 0
    cooldown: int = 0

@dataclass
class GameServer:
    server_id: str
    state: ServerState = ServerState.OFFLINE
    max_players: int = 100
    current_players: List[Player] = None
    import os




class GameEventSimulator:
    def __init__(self, config_json: str):
        self.config = config_json

        # Generate difficulties for maps
        self.maps = self._initialize_maps_with_difficulty_array()

        # Rest of the initialization remains the same
        self.servers = self._initialize_servers()
        self.players = self._initialize_players()

        logging.info(f"Initialized simulator with {len(self.servers)} servers, {len(self.players)} players")

        self.current_time_step = 0
        self.event_log = []

    def _generate_difficulty_array(self, map_config: Dict[str, Any]) -> List[float]:
        """
        Generate a difficulty array for a map.

        Supports different generation strategies:
        1. Linear progression
        2. Exponential increase
        3. Random with constraints
        """
        total_levels = map_config.get("total_levels", 5)
        generation_strategy = map_config.get("difficulty_strategy", "linear")

        if generation_strategy == "linear":
            base_difficulty = map_config.get("base_difficulty", 0.1)
            max_difficulty = map_config.get("max_difficulty", 1.0)
            return [
                base_difficulty
                + (max_difficulty - base_difficulty) * (level / (total_levels - 1))
                for level in range(total_levels)
            ]

        elif generation_strategy == "exponential":
            base_difficulty = map_config.get("base_difficulty", 0.1)
            max_difficulty = map_config.get("max_difficulty", 1.0)
            return [
                base_difficulty
                * (max_difficulty / base_difficulty) ** (level / (total_levels - 1))
                for level in range(total_levels)
            ]

        elif generation_strategy == "random":
            base_difficulty = map_config.get("base_difficulty", 0.1)
            max_difficulty = map_config.get("max_difficulty", 1.0)
            return [
                random.uniform(
                    base_difficulty
                    + (max_difficulty - base_difficulty)
                    * (level / (total_levels - 1))
                    * 0.8,
                    base_difficulty
                    + (max_difficulty - base_difficulty)
                    * (level / (total_levels - 1))
                    * 1.2,
                )
                for level in range(total_levels)
            ]

        else:
            raise ValueError(
                f"Unknown difficulty generation strategy: {generation_strategy}"
            )

    def _initialize_maps_with_difficulty_array(self) -> Dict[str, List[MapLevel]]:
        maps = {}
        for map_config in self.config.get("maps", []):
            difficulty_array = self._generate_difficulty_array(map_config)

            map_levels = [
                MapLevel(
                    map_name=map_config["name"],
                    level_number=level + 1,
                    difficulty_array=difficulty_array,
                )
                for level in range(len(difficulty_array))
            ]
            maps[map_config["name"]] = map_levels
        return maps

    def _initialize_servers(self) -> List[GameServer]:
        servers = []
        for server_config in self.config.get('servers', []):
            server = GameServer(
                server_id=server_config['server_id'],
                state=ServerState[server_config.get('initial_state', 'OFFLINE')],
                max_players=server_config.get('max_players', 100)
            )
            servers.append(server)
        return servers

    def _initialize_players(self) -> List[Player]:
        player_init_config = self.config.get('player_init')
        if player_init_config is None:
            raise ValueError("player_init configuration is missing")
        num_players = player_init_config.get('num_players')
        if num_players is None:
            raise ValueError("num_players is missing in player_init configuration")
        skill_level_range = player_init_config.get('skill_level_range')
        if skill_level_range is None:
            raise ValueError("skill_level_range is missing in player_init configuration, e.g. [0.1, 0.9]")

        players = []
        for player_config in range(num_players):
            player_id = f"player_{player_config}"
            skill_level = random.uniform(*skill_level_range)
            player = Player(
                player_id=player_id,
                skill_level=skill_level,
                deaths = 0
            )
            players.append(player)
        return players

    def _generate_event_count(self) -> int:
        """
        Generate event count based on online servers and logged in players.

        Uses config parameters for randomness and scaling.
        """
        online_servers = sum(1 for server in self.servers if server.state == ServerState.ONLINE)
        logged_in_players = sum(1 for player in self.players if player.state != PlayerState.OFFLINE)

        base_events = self.config.get('base_event_count', 10)
        event_variance = self.config.get('event_variance', 0.3)

        scaled_events = base_events * (online_servers + logged_in_players) / 2
        variance_range = scaled_events * event_variance

        return int(max(1, random.uniform(
            scaled_events - variance_range,
            scaled_events + variance_range
        )))

    def _calculate_level_progression(self, player: Player, map_level: MapLevel) -> Dict[str, Any]:
        """
        Determine if player advances or fails based on difficulty and skill.

        Incorporates out-of-band difficulty if specified in config.
        """
        out_of_band_difficulty = self.config.get('out_of_band_difficulty', {}).get(
            f"{map_level.map_name}_level_{map_level.level_number}"
        )

        difficulty = out_of_band_difficulty if out_of_band_difficulty is not None \
            else map_level.get_current_difficulty()

        progression_probability = player.skill_level / (difficulty + player.skill_level)

        return {
            'success': random.random() < progression_probability,
            'difficulty': difficulty
        }

    def _server_add_player(self, server, player):
        if server.current_players is None:
            server.current_players = []
        server.current_players.append(player)

    def run_step(self) -> List[Dict[str, Any]]:
        """
        Execute a single time step of the simulation, generating events.

        Returns a list of events in JSON-serializable format.
        """
        self.current_time_step += 1
        step_events = []

        # Generate server state transition events
        for server in self.servers:
            if random.random() < self.config.get('server_state_transition_prob'):
                server = random.choice(self.servers)
                old_state = server.state

                # Implement Markov state transition based on config probabilities
                transition_probs = self.config.get('server_state_transitions').get(
                    old_state.name, {}
                )
                new_state = ServerState[random.choices(
                    list(transition_probs.keys()),
                    weights=list(transition_probs.values())
                )[0]]

                server.state = new_state
                step_events.append({
                    'event_type': 'server_state_change',
                    'server_id': server.server_id,
                    'old_state': old_state.name,
                    'new_state': new_state.name,
                    'timestamp': self.current_time_step
                })

        event_count = self._generate_event_count()
        logging.debug(f"Drawing player {event_count} events for time step {self.current_time_step} out of {len(self.players)} players")
        for _ in range(event_count):
            # Generate player level progression/death events
            player = random.choice(self.players)
            if player.current_map and player.state == PlayerState.IN_GAME:
                current_map_levels = self.maps.get(player.current_map, [])
                current_level_obj = current_map_levels[player.current_level - 1]

                progression = self._calculate_level_progression(player, current_level_obj)

                event = {
                    'event_type': 'player_progression',
                    'player_id': player.player_id,
                    'map': player.current_map,
                    'current_level': player.current_level,
                    'success': progression['success'],
                    'difficulty': progression['difficulty'],
                    'timestamp': self.current_time_step
                }

                if progression['success'] and player.current_level < len(current_map_levels):
                    player.current_level += 1
                    event['new_level'] = player.current_level
                else:
                    player.state = PlayerState.OFFLINE
                    player.deaths += 1
                    if player.deaths > 3:
                        player.cooldown = player.deaths / 2 + 1
                    event['event_type'] = 'player_death'

                step_events.append(event)

            elif player.state == PlayerState.OFFLINE:
                # Player is offline, move to logged in state, depending on deaths
                if player.cooldown > 0:
                    player.cooldown -= 1

                if player.cooldown == 0:
                    player.state = PlayerState.LOGGED_IN
                    step_events.append({
                        'event_type': 'player_login',
                        'player_id': player.player_id,
                        'timestamp': self.current_time_step
                    })

            if player.state == PlayerState.LOGGED_IN:
                # Player is logged in, move to in-game state
                player.state = PlayerState.IN_GAME
                player.current_map = random.choice(list(self.maps.keys()))
                player.current_level = 1

                # add to server
                server = random.choice(self.servers)
                self._server_add_player(server, player)

                step_events.append({
                    'event_type': 'player_start_game',
                    'player_id': player.player_id,
                    'map': player.current_map,
                    'level': player.current_level,
                    'timestamp': self.current_time_step
                })


        self.event_log.extend(step_events)
        return step_events



if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get('PY_LOG', 'INFO').upper()
    )

    sim_config = {
        "servers": [
            {"server_id": "server_1", "initial_state": "ONLINE", "max_players": 100},
            {"server_id": "server_2", "initial_state": "OFFLINE", "max_players": 100},
        ],
        "player_init" : {
            "num_players": 10,
            "skill_level_range": [0.1, 0.9]
        },
        "base_event_count": 10,
        "event_variance": 0.3,
        "out_of_band_difficulty": {"Forest_level_3": 0.9},
        "maps": [
            {
                "name": "Forest",
                "total_levels": 5,
                "base_difficulty": 0.1,
                "max_difficulty": 1.0,
                "difficulty_strategy": "linear",  # Options: 'linear', 'exponential', 'random'
            },
            {
                "name": "Mountain",
                "total_levels": 7,
                "base_difficulty": 0.2,
                "max_difficulty": 1.2,
                "difficulty_strategy": "exponential",
            },
        ],
        "server_state_transition_prob": 0.1,
        "server_state_transitions": {
            "ONLINE": {"ONLINE": 0.97, "OFFLINE": 0.02, "MAINTENANCE": 0.01},
            "OFFLINE": {"ONLINE": 0.2, "OFFLINE": 0.7, "MAINTENANCE": 0.1},
            "MAINTENANCE": {"ONLINE": 0.1, "OFFLINE": 0.1, "MAINTENANCE": 0.8},
        },
    }
    simulator = GameEventSimulator(sim_config)

    # Run multiple simulation steps
    for _ in range(5):
        events = simulator.run_step()
        print(f"Generated {len(events)} events:")
        for event in events:
            print(json.dumps(event, indent=2))

