import gamelib
import random


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

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

        self.defense_library = self.get_defenses()

    def get_defenses(self):
        """
        Dictionary of defenses.
        """
        def make_build_list(build_order):
            build_list = []
            for unit_type, unit_order in build_order:
                build_list += [[unit_type, loc] for loc in unit_order]
            return build_list

        defense_library = {}

        filter_1 = [[0, 13], [1, 13], [2, 13], [3, 12], [4, 11], [5, 10], [22, 10], [23, 11], [24, 12], [25, 13], [26, 13], [27, 13]]
        destructor_1 = [[10, 9], [17, 9], [9, 9], [18, 9]]
        filter_2 = [[11, 10], [16, 10], [7, 10], [20, 10], [6, 10], [21, 10], [12, 10], [15, 10], [8, 10, ], [19, 10]]
        destructor_2 = [[13, 9], [14, 9], [12, 9], [15, 9], [11, 9], [16, 9]]
        defense_library['edge_attack'] = make_build_list([[FILTER, filter_1], [DESTRUCTOR, destructor_1], [FILTER, filter_2], [DESTRUCTOR, destructor_2]])

        filter_1 = [[0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [27, 13], [26, 12], [25, 11], [24, 10], [23, 9], [22, 8]]
        destructor_1 = [[11, 7], [16, 7], [13, 9], [14, 9]]
        filter_2 = [[12, 10], [15, 10]]
        destructor_2 = [[11, 9], [16, 9]]
        filter_3 = [[10, 10], [17, 10]]
        destructor_3 = [[9, 9], [18, 9]]
        filter_4 = [[8, 10], [19, 10]]
        destructor_4 = [[9, 9], [18, 9], [10, 8], [17, 8]]
        filter_5 = [[11, 10], [16, 10], [9, 10], [18, 10]]
        defense_library['inverted_triangle'] = make_build_list([[FILTER, filter_1], [DESTRUCTOR, destructor_1], [FILTER, filter_2], [DESTRUCTOR, destructor_2], [FILTER, filter_3], [DESTRUCTOR, destructor_3], [FILTER, filter_4], [DESTRUCTOR, destructor_4], [FILTER, filter_5]])

        return defense_library

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        # game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.defend(game_state)

        game_state.submit_turn()

    def defend(self, game_state):
        for unit_type, location in self.defense_library["inverted_triangle"]:
            if game_state.can_spawn(unit_type, location):
                game_state.attempt_spawn(unit_type, location)


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
