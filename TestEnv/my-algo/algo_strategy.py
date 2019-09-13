import gamelib
import random
import warnings  # NOQA
from sys import maxsize  # NOQA


class AlgoStrategy(gamelib.AlgoCore):
    """
    Most of the algo code you write will be in this file unless you create new
    modules yourself. Start by modifying the 'on_turn' function.

    Advanced strategy tips:

    Additional functions are made available by importing the AdvancedGameState
    class from gamelib/advanced.py as a replacement for the regular GameState class
    in game.py.

    You can analyze action frames by modifying algocore.py.

    The GameState.map object can be manually manipulated to create hypothetical
    board states. Though, we recommended making a copy of the map to preserve
    the actual current map state.
    """
    def __init__(self):
        super().__init__()
        random.seed()
        # friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]

    def _test_functions(self, game_state):
        # locations = game_state._get_all_map_locations()
        # gamelib.debug_write(locations)
        # my_defenders, enemy_defenders = game_state.get_all_defenders()
        # gamelib.debug_write(my_defenders, enemy_defenders)
        ratings = game_state.rate_attack_positions(0)
        # for rating in ratings:
            # gamelib.debug_write(rating)
        gamelib.debug_write(ratings)
        # game_state.find_path_to_edge([10, 3], game_state.game_map.TOP_LEFT)
        pass

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.my_game_state.MyGameState(self.config, turn_state)
        self._test_functions(game_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        # game_state.suppress_warnings(True)
        self.strategy(game_state)
        game_state.submit_turn()

    def strategy(self, game_state):
        """
        Make sure we have a good line of defense, with destructors behind filters.
        Leave middle open usually, but open sides when appropriate for attack.
        """
        self.read_game_state(game_state)
        self.bolster_defenses(game_state)
        self.deploy_attackers(game_state)

    def read_game_state(self, game_state):
        self.bits = game_state.get_resource(game_state.BITS)
        self.cores = game_state.get_resource(game_state.CORES)

    def bolster_defenses(self, game_state):
        self.x_gap = 16
        self.gaps = {}
        self.gaps[FILTER] = [[x, 13] for x in range(28) if (not game_state.contains_stationary_unit([x, 13])) and (x != self.x_gap)]
        self.gaps[DESTRUCTOR] = [[x, 12] for x in range(1, 27) if (not game_state.contains_stationary_unit([x, 12])) and (x != self.x_gap)]
        while self.cores >= 3 and len(self.gaps[FILTER]) > 0 and len(self.gaps[DESTRUCTOR]) > 0:
            if len(self.gaps[DESTRUCTOR]) > 22:
                self.build_random_defense(game_state, DESTRUCTOR)
            elif len(self.gaps[FILTER]) > 0:
                self.build_random_defense(game_state, FILTER)
            else:
                self.build_random_defense(game_state, DESTRUCTOR)

    def build_random_defense(self, game_state, defender_type):
        if (len(self.gaps[defender_type]) > 0):
            gap = self.gaps[defender_type][random.randint(0, len(self.gaps[defender_type])-1)]
            self.build_defense(game_state, defender_type, gap)

    def build_defense(self, game_state, defender_type, gap):
        if defender_type == DESTRUCTOR:
            if (gap in self.gaps[DESTRUCTOR]) and (self.cores >= 3):
                game_state.attempt_spawn(DESTRUCTOR, gap)
                self.gaps[DESTRUCTOR].remove(gap)
                self.cores -= 3
                filter_gap = gap
                filter_gap[1] += 1
                self.build_defense(game_state, FILTER, filter_gap)
                filter_gap[0] -= 1
                self.build_defense(game_state, FILTER, filter_gap)
                filter_gap[0] += 2
                self.build_defense(game_state, FILTER, filter_gap)
        elif defender_type == FILTER:
            if (gap in self.gaps[FILTER]) and (self.cores >= 1):
                self.cores -= 1
                game_state.attempt_spawn(FILTER, gap)
                self.gaps[FILTER].remove(gap)

    def deploy_attackers(self, game_state):
        if (self.bits < 15):
            return
        game_state.attempt_spawn(EMP, [12 + 3*random.randint(0, 1), 1], 5)


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
