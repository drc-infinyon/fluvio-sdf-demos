

# prompt

Create a data driven event generation simulator with a set of states for game servers, players on the server, and player activities for game levels. Use a markov state transition approach with different probabilities to transition between states.   Different instances of players should have individual probabilities for likelihood to advance game levels.

Game servers should have online, offline states.  IF online a game server will have a number of individual players logged on with some probability of logging  as well as an increased probability of logging out after not advancing a level

Include a set of events for players to purchase a set of game items with given labels and prices,  use a set of 30 item labels generally considered gaming decorative items in the category of "outfit skins", "hats",  "stickers", "dances"

The markov states and transition probabilities should be loaded from a data driven config. Events that can be output as
json should be generated as a simulation time step with random range of the number of events generated per fixed time step.
The range of event number should be somewhat random, but proportional to the number of servers online and players logged in.

The simulator should be able to be initialized with it's config data, then `server.run_step()` should cause a number of events to be generated.

