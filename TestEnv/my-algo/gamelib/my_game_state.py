import gamelib  # NOQA
from .advanced_game_state import AdvancedGameState


class MyGameState(AdvancedGameState):

    def _get_all_map_locations(self):
        '''Return a list of all legal positions on the map.'''
        return list(self.game_map)

    def _get_defenders(self, player):
        '''Return a list of defenders for a given player.'''
        defenders = []
        for location in self.game_map:
            unit = self.contains_stationary_unit(location)
            if unit and (unit.player_index == player):
                defenders.append(unit)
        return defenders

    def get_all_defenders(self):
        '''Return two lists of positions, one for my defenders and one for the enemy's.'''
        my_defenders = self._get_defenders(0)
        enemy_defenders = self._get_defenders(1)
        return my_defenders, enemy_defenders

    def find_defenders_along_path(self, path, player):
        '''Given a path traveled by an attacker, find all enemy defenders along the path.'''
        defenders = []
        for location in path:
            defenders.append(self.get_attackers(location, player))
        return defenders

    def rate_attack_positions(self, player):
        '''For each attack position, return a list of how many defenders are in range at each step.'''
        def rate(start_edge, end_edge):
            for location in self.game_map.get_edge_locations(start_edge):
                if self.contains_stationary_unit(location):
                    continue
                path = self.find_path_to_edge(location, end_edge)
                ratings.append([location, self.find_defenders_along_path(path, player)])

        ratings = []
        if player == 0:
            rate(self.game_map.BOTTOM_LEFT, self.game_map.TOP_RIGHT)
            rate(self.game_map.BOTTOM_RIGHT, self.game_map.TOP_LEFT)
        elif player == 1:
            rate(self.game_map.TOP_LEFT, self.game_map.BOTTOM_RIGHT)
            rate(self.game_map.TOP_RIGHT, self.game_map.BOTTOM_LEFT)
        return ratings

    def get_game_state_with_additional_blockers(self, blockers):
        '''Return the game state we would have if we added blockers at a given list of locations.'''
        pass
