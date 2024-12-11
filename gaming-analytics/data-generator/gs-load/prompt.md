

# prompt

Create a data driven event generation simulator with a set of states for game servers, players on the server, and player presence in different named game areas. Use a markov state transition approach with different probabilities to transition between states.

Game servers should have online, offline states, as well as track which players are being hosted on a particular server.

Include a set of events for players to move between areas. The simulator be able to receive a command to shutdown a server or direct one server to a consolidation server. If a game server has a directive to consolidate to another server,
when a player changes areas, they will move from one area in a server to a different area on the consolidation server.  If a server is being drained to another consolidation server, it will not accept new players to host.

The markov states and transition probabilities should be loaded from a data driven config. Events that can be output as
json should be generated as a simulation time step with random range of the number of events generated per fixed time step.
The range of event number should be somewhat random, but proportional to the number of servers online and players logged in.

The simulator should be able to be initialized with it's config data, then `server.run_step()` should cause a number of events to be generated.

